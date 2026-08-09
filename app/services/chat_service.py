from sqlalchemy.orm import Session,selectinload
from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage
from app.models.user import User
from app.ai.chat_engine import generate_response,stream_response
from fastapi import HTTPException
from app.ai.chat_graph import chat_graph
from langchain_core.messages import HumanMessage, AIMessage
import json

#------------------------------------------------------------
#Session CRUD
#-------------------------------------------------------------
#create session
def create_session(db:Session,user:User)->ChatSession:

    session=ChatSession(
        user_id=user.id,
        title="New Chat",
    )

    db.add(session)
    db.flush() #generate session.id without committing

    return session


#get session

def get_session(db:Session,session_id:int,user:User)->ChatSession | None:
    return(
        db.query(ChatSession)
        .options(selectinload(ChatSession.messages))
        .filter(
            ChatSession.id==session_id,
            ChatSession.user_id==user.id
        )
        .first()
    )

#save message
def save_message(db:Session,session:ChatSession,role:str,content:str):
    message=ChatMessage(
        session_id=session.id,
        role=role,
        content=content
    )

    db.add(message)
   

    return message

#load history
def get_messages(db:Session,session:ChatSession):
    return(
        db.query(ChatMessage)
        .filter(
            ChatMessage.session_id==session.id
        )
        .order_by(ChatMessage.created_at)
        .all()
    )

#get user sessions
def get_user_sessions(db:Session,user:User):
    return(
        db.query(ChatSession)
        .filter(ChatSession.user_id==user.id)
        .order_by(ChatSession.updated_at.desc())
        .all()
    )

#delete session

def delete_session(db:Sesion,session:ChatSession):
    db.delete(session)
    db.commit()



#----------------------HELPERS-------------------------------------
def _get_or_create_session(db:Session,user:User,session_id:int | None)->ChatSession:
    if session_id is None:
        return create_session(db,user)

    session=get_session(
        db,
        session_id,
        user
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Chat session not found"
        )

    return session


def _build_history(db:session,session:ChatSession,message:str):
    history=get_messages(db,session)

    history.append(
        ChatMessage(
            role="user",
            content=message
        )
    )

    return history


def _build_langchain_history(history):
    """
    Convert database ChatMessage objects
    into langchain messages.
    """

    messages=[]

    for message in history:
        if message.role=='user':
            messages.append(
                HumanMessage(content=message.content)
            )

        elif message.role=="assistant":
            messages.append(AIMessage(content=message.content))

    return messages


#----------------------------------------------------------------------
#process chat
#Chat Orchestration

def process_chat(db:Session,user:User,session_id:int | None,message:str):
    """
    Process a complete chat request
    """
    try:
        session=_get_or_create_session(
            db,
            user,
            session_id
        )

        #=======================================================
        #load conversation history
        #========================================================


        history=_build_history(
            db,
            session,
            message
        )


        #==================================================
        #Convert DB messages->langchain messages
        #===============================================

        langchain_history=_build_langchain_history(history)

        #run langraph

        result=chat_graph.invoke(
            {
                "messages":langchain_history,
                "route": "",
                "user_id": user.id,
            }
        )

        #generate AI response
        ai_response=result["messages"][-1].content



        #save both message
        save_message(
            db=db,
            session=session,
            role="user",
            content=message
        )

        save_message(
            db=db,
            session=session,
            role="assistant",
            content=ai_response
        )

        db.commit()

        return session.id, ai_response

    except Exception:
        db.rollback()
        raise


#------------------------------------------------------------------------------------------------


#Chat (Streaming)

#-----------------------------------------------------------------------------------------

def process_chat_stream(
    db:Session,
    user:User,
    message:str,
    session_id:int | None,
    
):
    session=_get_or_create_session(
        db,
        user,
        session_id
    )

    history=_build_history(
        db,
        session,
        message
    )

    generator=stream_response(history,user.id)

    def response_generator():
        full_response=""

        try:
            for chunk in generator:
                full_response+=chunk

                yield (
                    f"event:token\n"
                    f"data:{json.dumps({"content":chunk})}\n\n"
                )

            save_message(
                db,
                session,
                "user",
                message
            )

            save_message(
                db,
                session,
                "assistant",
                full_response

            )

            db.commit()

            yield(
                "event:done\n"
                "data:{}\n\n"
            )

        except Exception:
            db.rollback()
            yield(
                "event: error\n"
                f"data: {json.dumps({'message': 'AI generation failed'})}\n\n"
            )

    return session.id, response_generator()