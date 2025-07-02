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

import os
print(f"Starting application...")
print(f"Current directory: {os.getcwd()}")
print(f"Python path: {os.environ.get('PYTHONPATH', 'Not set')}")
print(f"PORT: {os.environ.get('PORT', 'Not set')}")

try:
    from bot.handlers.location import handle_help, handle_location, handle_start
    from config.settings import settings
    print("Successfully imported all modules")
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Directory contents: {os.listdir('.')}")
    if os.path.exists('bot'):
        print(f"Bot directory contents: {os.listdir('bot')}")
    if os.path.exists('config'):
        print(f"Config directory contents: {os.listdir('config')}")
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
    logger.info("Starting bot initialization...")
    
    # Check configuration
    if not settings.telegram_bot_token:
        logger.error("TELEGRAM_BOT_TOKEN is not set!")
        return
    
    if not settings.openai_api_key:
        logger.error("OPENAI_API_KEY is not set!")
        return
    
    logger.info(f"Bot token length: {len(settings.telegram_bot_token)}")
    logger.info(f"OpenAI key length: {len(settings.openai_api_key)}")
    logger.info(f"Webhook URL: {settings.webhook_url}")
    
    try:
        # Add handlers
        application.add_handler(CommandHandler("start", handle_start))
        application.add_handler(CommandHandler("help", handle_help))
        application.add_handler(
            MessageHandler(filters.LOCATION & ~filters.COMMAND, handle_location)
        )
        logger.info("Handlers added successfully")

        # Initialize application
        await application.initialize()
        logger.info("Application initialized")
        
        await application.start()
        logger.info("Application started")

        # Set webhook if URL is provided
        if settings.webhook_url:
            webhook_url = f"{settings.webhook_url}/webhook"
            await application.bot.set_webhook(webhook_url)
            logger.info(f"Webhook set to: {webhook_url}")
            
            # Get webhook info
            webhook_info = await application.bot.get_webhook_info()
            logger.info(f"Webhook info: {webhook_info}")
        else:
            logger.warning("No webhook URL provided, bot will not receive updates")

        logger.info("Bot started successfully")
        
    except Exception as e:
        logger.error(f"Error during bot startup: {e}")
        raise


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


@app.get("/config")
async def config_check():
    """Check configuration and environment."""
    return {
        "telegram_token_set": bool(settings.telegram_bot_token and len(settings.telegram_bot_token) > 10),
        "openai_key_set": bool(settings.openai_api_key and len(settings.openai_api_key) > 10),
        "webhook_url": settings.webhook_url,
        "environment": settings.environment,
        "port": settings.port,
        "log_level": settings.log_level,
    }


@app.get("/webhook/info")
async def webhook_info():
    """Get webhook information."""
    try:
        if application.bot:
            webhook_info = await application.bot.get_webhook_info()
            return {
                "webhook_info": {
                    "url": webhook_info.url,
                    "has_custom_certificate": webhook_info.has_custom_certificate,
                    "pending_update_count": webhook_info.pending_update_count,
                    "last_error_date": webhook_info.last_error_date,
                    "last_error_message": webhook_info.last_error_message,
                    "max_connections": webhook_info.max_connections,
                    "allowed_updates": webhook_info.allowed_updates,
                }
            }
        else:
            return {"error": "Bot not initialized"}
    except Exception as e:
        return {"error": str(e)}


@app.post("/webhook")
async def webhook(request: Request):
    """Handle Telegram webhook updates."""
    try:
        logger.info("Received webhook request")
        data = await request.json()
        logger.info(f"Webhook data: {data}")
        
        update = Update.de_json(data, application.bot)

        if update:
            logger.info(f"Processing update: {update.update_id}")
            await application.process_update(update)
        else:
            logger.warning("No update object created")

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
