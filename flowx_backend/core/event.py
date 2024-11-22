from flowx_backend.db.connection import connect_db, close_db
import logging

logger = logging.getLogger("aleaf")

async def startup_event():
    logger.info("The application has started!")
    await connect_db()

async def shutdown_event():
    logger.info("The application is shutting down!")
    await close_db()