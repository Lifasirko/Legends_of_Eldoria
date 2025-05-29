import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from bot.config import BOT_TOKEN

# Реєстрація хендлерів
from bot.handlers.start import register_handlers as register_start
from bot.handlers.profile import register_handlers as register_profile
from bot.handlers.rest import register_handlers as register_rest
from bot.handlers.hunt import register_handlers as register_hunt
from bot.handlers.quests import register_handlers as register_quests

async def main():
    # Use memory storage instead of Redis
    storage = MemoryStorage()
    
    dp = Dispatcher(storage=storage)
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )

    # Підключення хендлерів
    register_start(dp)
    register_profile(dp)
    register_rest(dp)
    register_hunt(dp)
    register_quests(dp)

    print("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 