from sqlalchemy.orm import Session
from app.models.chat_session import ChatSession
from app.models.chat_message imoport ChatMessage
from app.models.user import User


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
        session_id=session.id
        role=role,
        content=content
    )

    db.add(message)
    db.commit()

    return message

#load history
def get_message(db:Session,session:ChatSession):
    return(
        db.query(ChatMessage)
        .filter(
            ChatMessage.session_id==session.id
        )
        .order_by(ChatMessage.created_at)
        .all()
    )


