import os

AMAZON_ACCESS_KEY = os.getenv("AMAZON_ACCESS_KEY")
AMAZON_SECRET_KEY = os.getenv("AMAZON_SECRET_KEY")
AMAZON_ASSOCIATE_TAG = os.getenv("AMAZON_ASSOCIATE_TAG")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

MINIMUM_DISCOUNT = int(os.getenv("MINIMUM_DISCOUNT", 15))
SEARCH_KEYWORDS = os.getenv("SEARCH_KEYWORDS", "Electronics,Books,Video Games,Computers,laptop,smart bulb,speakers,fast charger,USB C,wireless charger,usb hub,docking station,power bank,rgb light,lightstrip,light rope,decor,Kitchen,Baby Clothes,Watches,Health,Crafts,smart home,gadgets,gaming,gaming consoles,playstation,xbox,nintendo switch").split(",")

TIMEZONE = os.getenv("TIMEZONE", "America/Santo_Domingo")
