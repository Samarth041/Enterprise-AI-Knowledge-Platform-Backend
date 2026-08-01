from fastapi import FastAPI
from app.api.routes.users import router as user_router
from app.core.config import settings
from app.api.routes.posts import router as post_router
from app.api.routes.auth import router as auth_router
from app.core.exceptions import http_exception_handler,global_exception_handler
from fastapi import HTTPException,Request
import time
from app.core.logging import logger
from fastapi.middleware.cors import CORSMiddleware



app=FastAPI(title=settings.APP_NAME )


app.add_exception_handler(HTTPException,http_exception_handler)

app.add_exception_handler(Exception,global_exception_handler)


#Middleware

@app.middleware("http")
async def log_requests(request:Request,call_next):
    start_time=time.time()

    logger.info(
        f"Incoming Request: {request.method} {request.url.path}"
    )

    response=await call_next(request)

    process_time=time.time()-start_time
    logger.info(
        f"Completed Request: {request.method} {request.url.path} in {process_time:.2f}s with status code {response.status_code}"
    )

    response.headers["X-Process-Time"]=str(process_time)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#user router
app.include_router(user_router)
app.include_router(post_router)
app.include_router(auth_router)
