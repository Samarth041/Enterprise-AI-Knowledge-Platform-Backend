from fastapi import FastAPI
from app.api.routes.users import router as user_router
from app.core.config import settings
from app.api.routes.posts import router as post_router
from app.api.routes.auth import router as auth_router


app=FastAPI(title=settings.APP_NAME )
#user router
app.include_router(user_router)
app.include_router(post_router)
app.include_router(auth_router)
