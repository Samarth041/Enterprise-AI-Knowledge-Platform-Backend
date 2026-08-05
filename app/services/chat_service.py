from sqlalchemy.orm import Session
from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage
from app.models.user import User
from app.ai.chat_engine import generate_response


#create session
def create_session(db:Session,user:User)->ChatSession:

    session=ChatSession(
        user_id=user.id,
        title="New Chat",
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


#get session

def get_session(db:Session,session_id:int,user:User)->ChatSession | None:
    return(
        db.query(ChatSession)
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
    db.commit()

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

#process chat

def process_chat(db:Session,user:User,session_id:int | None,message:str):
    """
    Process a complete chat request
    """

    if session_id is None:
        session=create_session(db,user)

    else:
        session=get_session(db,session_id,user)

        if session is None:
            raise HTTPException(
                status_code=404,
                detail="Chat Session not found"
            )

    #Save user message

    save_message(
        db=db,
        session=session,
        role="user",
        content=message
    )

    #load full conversation
    history=get_messages(
        db=db,
        session=session
    )

    #generate AI response

    ai_response=generate_response(history)

    #save assistant message

    save_message(
        db=db,
        session=session,
        role="assistant",
        content=ai_response
    )

    return session.id,ai_response








