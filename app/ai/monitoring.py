import logging
import time

logger=logging.getLogger("app.ai")

def start_ai_request():
    """
    Start timer for an AI request
    """

    return time.perf_counter()

def log_ai_request(
    *,
    user_id:int,
    route:str,
    start_time:float,
    success:bool=True,
    documents :int=0,
):
    """
    Log basic AI request metrics.
    """

    duration=time.perf_counter()-start_time

    logger.info(
        "AI request | "
        "user=%s | "
        "route=%s | "
        "duration=%.2fs | "
        "documents=%s | "
        "success=%s",
        user_id,
        route,
        duration,
        documents,
        success
    )