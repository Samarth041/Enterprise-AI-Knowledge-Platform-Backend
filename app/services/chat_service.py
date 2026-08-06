from sqlalchemy.orm import Session,selectinload
from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage
from app.models.user import User
from app.ai.chat_engine import generate_response
from fastapi import HTTPException

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


#process chat
#Chat Orchestration

def process_chat(db:Session,user:User,session_id:int | None,message:str):
    """
    Process a complete chat request
    """
    try:
        #get or create session
        if session_id is None:
            session=create_session(db,user)

        else:
            session=get_session(db,session_id,user)

            if session is None:
                raise HTTPException(
                    status_code=404,
                    detail="Chat session not found"
                )

        #load previous history'
        history=get_messages(
            db=db,
            session=session
        )

        #temporary current message

        current_message=ChatMessage(
            role="user",
            content=message
        )

        history.append(current_message)

        #generate AI response
        ai_response=generate_response(history)

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

        

    
    
