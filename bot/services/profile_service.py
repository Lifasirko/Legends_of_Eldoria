from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def get_profile_text(user_id: int) -> str:
    """Повертає текст профілю персонажа"""
    # TODO: Отримати дані з бази даних
    return (
        "👤 Профіль персонажа\n\n"
        "📊 Рівень: 1\n"
        "❤️ Здоров'я: 100/100\n"
        "⚔️ Атака: 10\n"
        "🛡 Захист: 5\n"
        "💰 Золото: 0\n"
        "✨ Досвід: 0/100"
    )

def get_profile_keyboard() -> InlineKeyboardMarkup:
    """Повертає клавіатуру профілю"""
    buttons = [
        [
            InlineKeyboardButton(text="📊 Характеристики", callback_data="profile:stats"),
            InlineKeyboardButton(text="🎒 Інвентар", callback_data="profile:inventory")
        ],
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data="menu:main")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def list_quests(user_id: int) -> list:
    # TODO: отримати список квестів з БД
    return []

async def accept_quest(user_id: int, quest_id: int) -> str:
    # TODO: прийняти квест
    return f"Квест #{quest_id} прийнято!" 