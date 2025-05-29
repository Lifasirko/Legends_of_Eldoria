from typing import List, Dict
from datetime import datetime

# Тимчасове сховище квестів (пізніше перенесемо в базу даних)
QUESTS = [
    {
        "id": 1,
        "title": "Перші кроки",
        "description": "Знайдіть 5 грибів у лісі",
        "reward": {"gold": 100, "exp": 50},
        "requirements": {"level": 1},
        "type": "gathering"
    },
    {
        "id": 2,
        "title": "Охоронець лісу",
        "description": "Перемогти 3 вовків",
        "reward": {"gold": 200, "exp": 100},
        "requirements": {"level": 2},
        "type": "combat"
    }
]

async def list_quests(user_id: int) -> str:
    """Повертає список доступних квестів"""
    text = "📜 Доступні квести:\n\n"
    
    for quest in QUESTS:
        text += f"🔹 {quest['title']}\n"
        text += f"📝 {quest['description']}\n"
        text += f"💰 Нагорода: {quest['reward']['gold']} золота, {quest['reward']['exp']} досвіду\n"
        text += f"📊 Рівень: {quest['requirements']['level']}+\n\n"
    
    text += "Натисніть на квест, щоб прийняти його"
    return text

async def accept_quest(user_id: int, quest_id: int) -> str:
    """Приймає квест для користувача"""
    quest = next((q for q in QUESTS if q["id"] == quest_id), None)
    if not quest:
        return "❌ Квест не знайдено"
    
    # TODO: Перевірка рівня персонажа
    # TODO: Збереження активного квесту в базі даних
    
    return f"✅ Ви прийняли квест: {quest['title']}"

async def check_quest_progress(user_id: int, quest_id: int) -> Dict:
    """Перевіряє прогрес квесту"""
    # TODO: Реалізувати перевірку прогресу
    return {"completed": False, "progress": 0}

async def complete_quest(user_id: int, quest_id: int) -> str:
    """Завершує квест і видає нагороду"""
    # TODO: Реалізувати завершення квесту
    return "Квест завершено" 