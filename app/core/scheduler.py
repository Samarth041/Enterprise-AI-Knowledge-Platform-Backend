from apscheduler.schedulers.background import BackgroundScheduler
from app.db.database import SessionLocal
from app.core.logging import logger
from app.services.refresh_token_service import cleanup_expired_refresh_tokens

scheduler = BackgroundScheduler()

def cleanup_job():
    logger.info("Running refresh token cleanup job...")
    db=SessionLocal()

    try:
        cleanup_expired_refresh_tokens(db)

    finally:
        db.close()

def start_scheduler():
    scheduler.add_job(cleanup_job,trigger="cron", hour=2,minute=0) #run every day at 2:00 AM
    scheduler.start()