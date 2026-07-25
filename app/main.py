from fastapi import FastAPI
from app.api.routes.users import router as user_router
from app.core.config import settings
from app.api.routes.posts import router as post_router


app=FastAPI(title=settings.app_name)
#user router
app.include_router(user_router)
app.include_router(post_router)
