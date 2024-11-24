from os import getenv

from dotenv import load_dotenv

load_dotenv()


API_ID = (getenv("API_ID"))
API_HASH = getenv("API_HASH")

BOT_TOKEN = getenv("BOT_TOKEN")
MONGO_DB_URI = getenv("MONGO_DB_URI", None)

OWNER_ID = (getenv("OWNER_ID", 7396541413))
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/PBX_CHAT")

MUST_JOIN = getenv("MUST_JOIN", "PBX_CHAT")
