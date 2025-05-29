from bot.utils.time_parser import parse_duration
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Optional

# Тимчасове сховище для відпочинку (пізніше перенесемо в базу даних)
RESTING_USERS: Dict[int, datetime] = {}

def calculate_rest(current_hp: int, max_hp: int, current_mp: int, max_mp: int, hours: float) -> tuple[int,int]:
    """
    Обчислює нові значення HP та MP після відпочинку.
    """
    rest_hp = min(max_hp, current_hp + int(max_hp * 0.1 * hours))
    rest_mp = min(max_mp, current_mp + int(max_mp * 0.15 * hours))
    return rest_hp, rest_mp

async def rest(user_id: int, duration: str = "1h") -> str:
    """Обробка відпочинку персонажа"""
    # Перевірка чи персонаж вже відпочиває
    if user_id in RESTING_USERS:
        end_time = RESTING_USERS[user_id]
        if datetime.now() < end_time:
            remaining = end_time - datetime.now()
            return f"⏳ Ви вже відпочиваєте. Залишилось: {remaining.seconds // 60} хвилин"
        else:
            del RESTING_USERS[user_id]
    
    # Парсинг тривалості
    try:
        hours = int(duration.replace("h", ""))
    except ValueError:
        hours = 1
    
    # Встановлення таймера
    end_time = datetime.now() + timedelta(hours=hours)
    RESTING_USERS[user_id] = end_time
    
    # TODO: Зберегти стан в базі даних
    
    return (
        f"😴 Ви почали відпочивати на {hours} годин.\n"
        f"⏰ Час закінчення: {end_time.strftime('%H:%M')}\n\n"
        "Поверніться після відпочинку, щоб отримати бонуси!"
    )

async def check_rest_status(user_id: int) -> Optional[Dict]:
    """Перевірка статусу відпочинку"""
    if user_id not in RESTING_USERS:
        return None
    
    end_time = RESTING_USERS[user_id]
    if datetime.now() >= end_time:
        # Відпочинок завершено
        del RESTING_USERS[user_id]
        return {
            "completed": True,
            "energy_restored": 100,  # TODO: Розрахувати на основі часу
            "bonus_exp": 50  # TODO: Розрахувати на основі часу
        }
    
    return {
        "completed": False,
        "remaining_minutes": (end_time - datetime.now()).seconds // 60
    }

async def rest_service(user_id: int, args: str) -> str:
    hours = parse_duration(args) or 1.0
    # TODO: отримати з БД current_hp, max_hp, current_mp, max_mp для user_id
    # Для демонстрації використовуємо заглушки:
    current_hp, max_hp = 50, 100
    current_mp, max_mp = 20, 50
    new_hp, new_mp = calculate_rest(current_hp, max_hp, current_mp, max_mp, hours)
    hp_diff = new_hp - current_hp
    mp_diff = new_mp - current_mp
    # TODO: оновити БД
    return f"🛌 Відпочили {hours:.1f}h: HP +{hp_diff} ({current_hp}->{new_hp}), MP +{mp_diff} ({current_mp}->{new_mp})" 