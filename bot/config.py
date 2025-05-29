import os
from dotenv import load_dotenv

# Завантаження змінних середовища
load_dotenv()

# Налаштування бота
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Налаштування Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Налаштування бази даних
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///game.db") 