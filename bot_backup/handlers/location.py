"""Location handler for processing user location messages."""

import logging

from telegram import Update
from telegram.ext import ContextTypes

from bot.services.openai_client import openai_client
from bot.services.rate_limiter import rate_limiter

logger = logging.getLogger(__name__)


async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle location messages from users.

    Args:
        update: Telegram update object
        context: Callback context
    """
    if not update.message or not update.message.location:
        return

    user = update.effective_user
    if not user:
        return

    location = update.message.location
    chat_id = update.effective_chat.id
    user_id = user.id

    logger.info(
        f"Received location from user {user_id}: {location.latitude}, {location.longitude}"
    )

    # Check rate limit
    if not await rate_limiter.check_rate_limit(user_id):
        await update.message.reply_text(
            "⏳ Пожалуйста, подождите немного перед следующим запросом. "
            "Можно отправлять не более одной локации в 5 секунд."
        )
        return

    # Acquire rate limit slot
    await rate_limiter.acquire(user_id)

    # Send typing action
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    # Get fact from OpenAI
    fact = await openai_client.get_location_fact(
        latitude=location.latitude,
        longitude=location.longitude,
        language="ru",  # Default to Russian for MVP
    )

    if fact:
        await update.message.reply_text(f"📍 {fact}")
    else:
        await update.message.reply_text(
            "😔 Не смог найти интересный факт об этом месте. "
            "Попробуйте отправить другую точку!"
        )


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /start command.

    Args:
        update: Telegram update object
        context: Callback context
    """
    welcome_message = (
        "👋 Привет! Я бот, который расскажет интересные факты о любом месте.\n\n"
        "📍 Просто отправьте мне свою геолокацию, и я найду что-то необычное "
        "в радиусе 500 метров от вас!\n\n"
        "Используйте кнопку 📎 и выберите «Локация» для отправки."
    )

    if update.message:
        await update.message.reply_text(welcome_message)


async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /help command.

    Args:
        update: Telegram update object
        context: Callback context
    """
    help_message = (
        "ℹ️ Как использовать бота:\n\n"
        "1. Нажмите кнопку 📎 (скрепка)\n"
        "2. Выберите «Локация» или «Геопозиция»\n"
        "3. Отправьте свою текущую локацию\n"
        "4. Получите интересный факт!\n\n"
        "⚡ Ограничения: не более 1 запроса в 5 секунд"
    )

    if update.message:
        await update.message.reply_text(help_message)
