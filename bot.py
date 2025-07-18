import asyncio
from datetime import datetime
from pytz import timezone
from telegram.ext import ApplicationBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import config
import random
from amazon_api import search_amazon_deals
from utils import init_db, is_posted_recently, save_posted

init_db()
application = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()
bot = application.bot
scheduler = AsyncIOScheduler(timezone=timezone(config.TIMEZONE))

async def post_deal():
    max_attempts = 5
    attempt = 0
    deals = []

    while not deals and attempt < max_attempts:
        keyword = random.choice(config.SEARCH_KEYWORDS)
        print(f"🎯 Attempt {attempt + 1}: Searching keyword '{keyword}'")
        results = search_amazon_deals(
            keywords=keyword,
            min_discount=config.MINIMUM_DISCOUNT
        )

        # ✅ Filter out deals already posted in the last 24h
        deals = [deal for deal in results if not is_posted_recently(deal['asin'])]
        attempt += 1

    if not deals:
        print("❌ No new deals found after multiple attempts.")
        return

    deal = random.choice(deals)

    # build and send the post, then call save_posted(deal['asin'])
    original = deal.get('original_price', 'N/A')
    discounted = deal['price']
    discount = deal['discount']
    
    caption = (
        f"🔥 <b>{deal['title']}</b>\n"
        f"\n"
        f"💰<b>AHORA: {discounted}</b>\n"
        f"Antes: {original} → (Ahorras {discount}%)\n"
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

async def scheduled_job():
    print("⏰ scheduled_job triggered")
    now = datetime.now(timezone(config.TIMEZONE)).time()
    start_time = datetime.strptime('08:00', '%H:%M').time()
    end_time = datetime.strptime('23:00', '%H:%M').time()
    if start_time <= now <= end_time:
        await post_deal()
    else:
        print("🛑 Outside posting hours.")

async def main():
    print("Bot starting...")
    await application.initialize()
    await application.start()

    scheduler.add_job(
        scheduled_job,
        trigger='interval',
        minutes=5,
        next_run_time=datetime.now(timezone(config.TIMEZONE))
    )
    scheduler.start()

    print("✅ Scheduler started and bot is running.")
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())
