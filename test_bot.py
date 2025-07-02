#!/usr/bin/env python3
"""Test script to check bot configuration and webhook."""

import asyncio
import os
import sys
from telegram import Bot
import httpx

async def test_bot():
    """Test bot configuration."""
    
    # Check environment variables
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    webhook_url = os.getenv('WEBHOOK_URL')
    
    print("=== Bot Configuration Test ===")
    print(f"Bot token set: {'Yes' if bot_token else 'No'}")
    print(f"Webhook URL set: {'Yes' if webhook_url else 'No'}")
    
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN not set!")
        return
    
    if len(bot_token) < 10:
        print("❌ TELEGRAM_BOT_TOKEN seems invalid!")
        return
        
    print(f"Bot token length: {len(bot_token)}")
    print(f"Webhook URL: {webhook_url}")
    
    # Test bot connection
    try:
        bot = Bot(token=bot_token)
        me = await bot.get_me()
        print(f"✅ Bot connected successfully!")
        print(f"Bot name: {me.first_name}")
        print(f"Bot username: @{me.username}")
        
        # Check webhook
        webhook_info = await bot.get_webhook_info()
        print(f"\n=== Webhook Info ===")
        print(f"Webhook URL: {webhook_info.url}")
        print(f"Pending updates: {webhook_info.pending_update_count}")
        print(f"Last error: {webhook_info.last_error_message}")
        
        # Set webhook if URL provided
        if webhook_url:
            full_webhook_url = f"{webhook_url}/webhook"
            await bot.set_webhook(url=full_webhook_url)
            print(f"✅ Webhook set to: {full_webhook_url}")
            
            # Check again
            webhook_info = await bot.get_webhook_info()
            print(f"New webhook URL: {webhook_info.url}")
        
    except Exception as e:
        print(f"❌ Error testing bot: {e}")

if __name__ == "__main__":
    # You can set these manually for testing
    if len(sys.argv) > 1:
        os.environ['TELEGRAM_BOT_TOKEN'] = sys.argv[1]
    if len(sys.argv) > 2:
        os.environ['WEBHOOK_URL'] = sys.argv[2]
    
    asyncio.run(test_bot()) 