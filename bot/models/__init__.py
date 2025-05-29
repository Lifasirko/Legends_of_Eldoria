import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .base import Base, create_tables
from .initial_data import init_initial_data

# Завантаження змінних середовища
load_dotenv()

# Отримання URL бази даних з змінних середовища
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///game.db")

# Створення асинхронного двигуна
engine = create_async_engine(DATABASE_URL, echo=True)

# Створення фабрики сесій
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def init_db():
    """Ініціалізація бази даних"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Ініціалізація початкових даних
    async with async_session() as session:
        await init_initial_data(session)

async def get_session():
    """Отримання сесії бази даних"""
    async with async_session() as session:
        yield session 