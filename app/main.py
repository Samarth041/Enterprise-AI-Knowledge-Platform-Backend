from fastapi import FastAPI
from app.api.routes.users import router as user_router
from app.core.config import settings


app=FastAPI(title=settings.app_name)

app.include_router(user_router)
