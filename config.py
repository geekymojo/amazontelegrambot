import os

AMAZON_ACCESS_KEY = os.getenv("AMAZON_ACCESS_KEY")
AMAZON_SECRET_KEY = os.getenv("AMAZON_SECRET_KEY")
AMAZON_ASSOCIATE_TAG = os.getenv("AMAZON_ASSOCIATE_TAG")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

MINIMUM_DISCOUNT = int(os.getenv("MINIMUM_DISCOUNT", 15))
SEARCH_KEYWORDS = os.getenv("SEARCH_KEYWORDS", "Electronics,Books,Video Games,Computers,Home And Kitchen,Baby Clothes,Watches,Health,Arts And Crafts,smart home,gadgets,gaming,gaming consoles,playstation game,xbox game,nintendo switch game").split(",")

TIMEZONE = os.getenv("TIMEZONE", "America/Santo_Domingo")
