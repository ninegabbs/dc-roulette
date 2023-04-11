import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
DB_NAME = os.getenv("DB_NAME", "dc-roulette.db")
DATETIME_FORMAT = os.getenv("DATETIME_FORMAT", "%Y-%m-%d %H:%M:%S")
GAME_NAME = os.getenv("GAME_NAME", "Rouletteverse")
ROUND_DURATION_S = os.getenv("ROUND_DURATION_S", "120")
