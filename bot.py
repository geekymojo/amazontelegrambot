import asyncio
from utils import init_db
from telegram import Bot
from telegram.ext import Application
import config

async def post_deal():
    # Placeholder for actual posting logic
    print("🟢 Bot is running and would post a deal now...")

async def main():
    init_db()
    await post_deal()

if __name__ == "__main__":
    asyncio.run(main())
