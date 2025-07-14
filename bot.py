import asyncio
from datetime import datetime
from pytz import timezone
from telegram.ext import ApplicationBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import config
import random
from amazon_api import search_amazon_deals
from utils import init_db, was_recently_posted, mark_as_posted

scheduler = AsyncIOScheduler(timezone=timezone(config.TIMEZONE))

async def post_deal(app):
    bot = app.bot
    max_attempts = 5
    attempt = 0
    deals = []

    while not deals and attempt < max_attempts:
        keyword = random.choice(config.SEARCH_KEYWORDS)
        print(f"🎯 Attempt {attempt+1}: Searching keyword '{keyword}'")
        deals = search_amazon_deals(
            keywords=keyword,
            min_discount=config.MINIMUM_DISCOUNT
        )
        attempt += 1

    if not deals:
        print("❌ No deals found after multiple attempts.")
        return

        deal = random.choice(deals)
        original = deal.get('original_price', 'N/A')
        discounted = deal['price']
        discount = deal['discount']
    
        caption = (
            parse_mode="HTML"
            f"🔥 <b>{deal['title']}</b><br>"
            f"<br>"
            f"💰<b>AHORA:{discounted} </b><br>"
            f"Antes: {original} → (Ahorras {discount}%)<br>"
            f"🔗 <a href='{deal['url']}'>VER OFERTA</a>"
            )
    try:
        await bot.send_photo(
            chat_id=config.TELEGRAM_CHANNEL_ID,
            photo=deal['image'],
            caption=caption,
            parse_mode="HTML"
        )
        print(f"✅ Posted: {deal['title']}")
        save_posted(deal['asin'])

    except Exception as e:
        print(f"❌ Failed to post to Telegram: {e}")

async def scheduled_job(app):
    print("⏰ scheduled_job triggered")
    now = datetime.now(timezone(config.TIMEZONE)).time()
    start_time = datetime.strptime('08:00', '%H:%M').time()
    end_time = datetime.strptime('22:00', '%H:%M').time()
    if start_time <= now <= end_time:
        await post_deal(app)
    else:
        print("🛑 Outside posting hours.")

async def main():
    print("🚀 Bot starting...")
    init_db()
    app = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()
    await app.initialize()
    await app.start()

    scheduler.add_job(
        scheduled_job,
        trigger='interval',
        minutes=5,
        next_run_time=datetime.now(timezone(config.TIMEZONE)),
        args=[app]
    )
    scheduler.start()

    print("✅ Scheduler started and bot is running.")
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())
