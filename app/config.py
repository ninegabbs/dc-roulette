import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
ACTIVE_CHANNEL = os.getenv("ACTIVE_CHANNEL", "dc-roulette")
DB_NAME = os.getenv("DB_NAME", "dc-roulette.db")
DATETIME_FORMAT = os.getenv("DATETIME_FORMAT", "%Y-%m-%d %H:%M:%S")
