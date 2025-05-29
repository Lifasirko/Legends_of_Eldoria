from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu() -> InlineKeyboardMarkup:
    """Create main menu keyboard"""
    buttons = [
        [
            InlineKeyboardButton(text="👤 Профіль", callback_data="profile"),
            InlineKeyboardButton(text="🏕 Відпочинок", callback_data="rest")
        ],
        [
            InlineKeyboardButton(text="🗡 Полювання", callback_data="hunt"),
            InlineKeyboardButton(text="📜 Квести", callback_data="quests")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons) 