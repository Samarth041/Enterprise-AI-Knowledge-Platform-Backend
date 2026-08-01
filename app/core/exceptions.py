from fastapi import Request,HTTPException
from fastapi.responses import JSONResponse
from app.core.logging import logger

async def http_exception_handler(request:Request,exc:HTTPException):

    logger.warning(
        f"{request.method} {request.url.path}-> "
        f"{exc.status_code}: {exc.detail}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success":False,
            "message":exc.detail
        }
    )


async def global_exception_handler(request:Request,exc:Exception):

    logger.exception(
        f"Unhandled exception on {request.method} {request.url.path}"
    )
    return JSONResponse(
        status_code=500,
        content={
            "success":False,
            "message":"Internal Server Error"
        }
    )