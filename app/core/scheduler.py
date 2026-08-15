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

    except Exception:
        logger.exception("Error while cleaning up expired refresh tokens")

    finally:
        db.close()

def start_scheduler():
    if scheduler.running:
        return

    scheduler.add_job(
        cleanup_job,
        "interval",
        minutes=5,
        id="cleanup_job",
        replace_existing=True
    )

    scheduler.start()

    logger.info("Background scheduler started")

def stop_scheduler():
    if not scheduler.running:
        return

    scheduler.shutdown(wait=False)

    logger.info("Background scheduler stopped")                                       