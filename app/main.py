from fastapi import FastAPI
from app.api.routes.users import router as user_router

app=FastAPI(title="Enterprise AI knowledge Platform")

app.include_router(user_router)
