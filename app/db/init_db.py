from app.db.database import Base,engine

#Import all models so SQLAchemy knows about them

from app.models.user import User

Base.metadata.create_all(bind=engine)

print("Database and tables created successfully.")