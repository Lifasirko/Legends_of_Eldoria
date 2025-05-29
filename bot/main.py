import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from bot.config import BOT_TOKEN, REDIS_HOST, REDIS_PORT
from bot.handlers.start import register_handlers as register_start
from bot.models import init_db

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    # Ініціалізація бази даних
    await init_db()
    
    # Ініціалізація бота
    storage = RedisStorage.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=storage)
    
    # Реєстрація хендлерів
    register_start(dp)
    
    # Запуск бота
    logger.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 