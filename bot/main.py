"""Main FastAPI application for the Location TG Bot."""

import logging
import sys

from fastapi import FastAPI, Request, Response
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

try:
    from bot.handlers.location import handle_help, handle_location, handle_start
    from config.settings import settings
except ImportError as e:
    print(f"Import error: {e}")
    import os
    print(f"Current directory: {os.getcwd()}")
    print(f"Directory contents: {os.listdir('.')}")
    raise

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, settings.log_level, logging.INFO),
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Location TG Bot", version="1.0.0")

# Create Telegram application
application = Application.builder().token(settings.telegram_bot_token).build()


@app.on_event("startup")
async def startup():
    """Initialize the bot on startup."""
    # Add handlers
    application.add_handler(CommandHandler("start", handle_start))
    application.add_handler(CommandHandler("help", handle_help))
    application.add_handler(
        MessageHandler(filters.LOCATION & ~filters.COMMAND, handle_location)
    )

    # Initialize application
    await application.initialize()
    await application.start()

    # Set webhook if URL is provided
    if settings.webhook_url:
        webhook_url = f"{settings.webhook_url}/webhook"
        await application.bot.set_webhook(webhook_url)
        logger.info(f"Webhook set to: {webhook_url}")
    else:
        logger.warning("No webhook URL provided, bot will not receive updates")

    logger.info("Bot started successfully")


@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown."""
    await application.stop()
    await application.shutdown()
    logger.info("Bot stopped")


@app.get("/")
async def root():
    """Root endpoint."""
    return {"status": "ok", "bot": "Location TG Bot"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/webhook")
async def webhook(request: Request):
    """Handle Telegram webhook updates."""
    try:
        data = await request.json()
        update = Update.de_json(data, application.bot)

        if update:
            await application.process_update(update)

        return Response(status_code=200)

    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return Response(status_code=200)  # Always return 200 to avoid Telegram retries


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "bot.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.environment == "development",
    )
