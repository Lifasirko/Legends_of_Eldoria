from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, List
from sqlalchemy import select
from ..models.base import Resource, Enemy, Player, Track

# Тимчасове сховище для боїв та досліджень
ACTIVE_BATTLES: Dict[int, Dict] = {}
EXPLORATION_RESULTS: Dict[int, Dict] = {}
ACTIVE_TRACKS: Dict[int, Dict] = {}

# Можливі ресурси та їх шанс появи
RESOURCES = {
    "гриби": {"chance": 0.3, "min": 1, "max": 3},
    "гілки": {"chance": 0.4, "min": 1, "max": 5},
    "трава": {"chance": 0.5, "min": 1, "max": 4},
    "каміння": {"chance": 0.2, "min": 1, "max": 2},
}

# Можливі вороги та їх характеристики
ENEMIES = {
    "вовк": {
        "name": "Вовк",
        "hp": 50,
        "attack": 8,
        "defense": 3,
        "exp": 20,
        "gold": 15,
        "chance": 0.3,
        "tracks": "сліди вовка"
    },
    "ведмідь": {
        "name": "Ведмідь",
        "hp": 100,
        "attack": 15,
        "defense": 8,
        "exp": 40,
        "gold": 30,
        "chance": 0.1,
        "tracks": "сліди ведмедя"
    },
    "бандит": {
        "name": "Бандит",
        "hp": 80,
        "attack": 12,
        "defense": 5,
        "exp": 35,
        "gold": 50,
        "chance": 0.2,
        "tracks": "сліди людини"
    }
}

def calculate_effective_dmg(atk: int, def_: int) -> int:
    """
    Обчислення ефективного урону без випадковості.
    Формула: floor(atk * 100 / (100 + def_)).
    """
    return (atk * 100) // (100 + def_)

def calculate_final_dmg(atk: int, def_: int, variation_percent: float = 0.05, random_factor: int = 0) -> int:
    """
    Обчислення фінального урону з варіацією.
    """
    effective = calculate_effective_dmg(atk, def_)
    return effective + random_factor

def simulate_fight(player: dict, monster: dict, random_factor: int = 0) -> tuple[list[tuple[str,int]], bool]:
    """
    Проста симуляція бою: гравець атакує першим.
    Повертає логи ходів та результат (True якщо гравець виграв).
    """
    logs = []
    p_hp, m_hp = player['hp'], monster['hp']
    while p_hp > 0 and m_hp > 0:
        dmg = calculate_final_dmg(player['atk'], monster['def'], random_factor=random_factor)
        m_hp -= dmg
        logs.append(('player', dmg))
        if m_hp <= 0:
            break
        dmg_m = calculate_final_dmg(monster['atk'], player['def'], random_factor=random_factor)
        p_hp -= dmg_m
        logs.append(('monster', dmg_m))
    return logs, p_hp > 0

async def get_available_resources(session) -> List[Dict]:
    """Отримання доступних ресурсів з бази даних"""
    query = select(Resource)
    result = await session.execute(query)
    resources = result.scalars().all()
    return [
        {
            "name": r.name,
            "chance": r.spawn_chance,
            "min": r.min_amount,
            "max": r.max_amount,
            "description": r.description
        }
        for r in resources
    ]

async def get_available_enemies(session) -> List[Dict]:
    """Отримання доступних ворогів з бази даних"""
    query = select(Enemy)
    result = await session.execute(query)
    enemies = result.scalars().all()
    return [
        {
            "name": e.name,
            "hp": e.hp,
            "attack": e.attack,
            "defense": e.defense,
            "exp": e.exp,
            "gold": e.gold,
            "chance": e.spawn_chance,
            "tracks": e.track_description
        }
        for e in enemies
    ]

async def get_player_tracks(session, user_id: int) -> List[Dict]:
    """Отримання слідів інших гравців"""
    query = select(Track).where(Track.player_id != user_id)
    result = await session.execute(query)
    tracks = result.scalars().all()
    return [
        {
            "player_id": t.player_id,
            "location": t.location,
            "time": t.created_at,
            "type": "player"
        }
        for t in tracks
    ]

async def quick_hunt(user_id: int, session) -> Tuple[str, InlineKeyboardMarkup]:
    """Дослідження території"""
    # Перевірка чи персонаж вже в бою
    if user_id in ACTIVE_BATTLES:
        battle = ACTIVE_BATTLES[user_id]
        if datetime.now() < battle["end_time"]:
            remaining = battle["end_time"] - datetime.now()
            return (
                f"⚔️ Ви вже в бою!\n"
                f"⏳ Залишилось: {remaining.seconds // 60} хвилин\n"
                f"❤️ Ваше здоров'я: {battle['player_hp']}\n"
                f"❤️ Здоров'я ворога: {battle['enemy_hp']}",
                battle["keyboard"]
            )
        else:
            del ACTIVE_BATTLES[user_id]
    
    # Отримання даних з бази
    resources = await get_available_resources(session)
    enemies = await get_available_enemies(session)
    player_tracks = await get_player_tracks(session, user_id)
    
    # Шанс знайти ресурси
    found_resources = []
    for resource in resources:
        if random.random() < resource["chance"]:
            amount = random.randint(resource["min"], resource["max"])
            found_resources.append(f"{amount} {resource['name']}")
    
    # Шанс знайти ворога
    enemy = None
    for enemy_data in enemies:
        if random.random() < enemy_data["chance"]:
            enemy = enemy_data
            break
    
    # Шанс знайти сліди
    tracks = []
    if not enemy:
        # Сліди ворогів
        for enemy_data in enemies:
            if random.random() < 0.4:
                tracks.append({
                    "type": "enemy",
                    "description": enemy_data["tracks"],
                    "enemy": enemy_data
                })
        
        # Сліди гравців
        for track in player_tracks:
            if random.random() < 0.3:
                tracks.append({
                    "type": "player",
                    "description": f"Сліди гравця в локації {track['location']}",
                    "player_id": track["player_id"]
                })
    
    # Формування повідомлення
    text = "🔍 Ви досліджуєте територію...\n\n"
    
    if found_resources:
        text += "📦 Знайдено ресурси:\n" + "\n".join(f"• {r}" for r in found_resources) + "\n\n"
    
    if tracks:
        text += "👣 Ви помітили сліди:\n"
        for track in tracks:
            text += f"• {track['description']}\n"
        text += "\n"
    
    if enemy:
        text += (
            f"⚠️ Ви натрапили на {enemy['name']}!\n\n"
            f"❤️ Ваше здоров'я: 100\n"  # TODO: Отримати з БД
            f"❤️ Здоров'я ворога: {enemy['hp']}\n"
            f"⚔️ Атака ворога: {enemy['attack']}\n"
            f"🛡 Захист ворога: {enemy['defense']}\n\n"
            "Оберіть дію:"
        )
        
        # Створення бою
        battle = {
            "enemy": enemy,
            "player_hp": 100,  # TODO: Отримати з БД
            "enemy_hp": enemy["hp"],
            "end_time": datetime.now() + timedelta(minutes=5),
            "keyboard": None
        }
        
        buttons = [
            [
                InlineKeyboardButton(text="⚔️ Атакувати", callback_data="hunt:attack"),
                InlineKeyboardButton(text="🛡 Захищатися", callback_data="hunt:defend")
            ],
            [
                InlineKeyboardButton(text="🏃 Втекти", callback_data="hunt:flee"),
                InlineKeyboardButton(text="🔙 Назад", callback_data="menu:main")
            ]
        ]
        kb = InlineKeyboardMarkup(inline_keyboard=buttons)
        battle["keyboard"] = kb
        ACTIVE_BATTLES[user_id] = battle
    elif tracks:
        # Кнопки для слідів
        buttons = []
        for i, track in enumerate(tracks):
            buttons.append([
                InlineKeyboardButton(
                    text=f"👣 Піти за слідами: {track['description']}",
                    callback_data=f"tracks:follow:{i}"
                )
            ])
        buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="menu:main")])
        kb = InlineKeyboardMarkup(inline_keyboard=buttons)
        
        # Зберігаємо інформацію про сліди
        ACTIVE_TRACKS[user_id] = {
            "tracks": tracks,
            "keyboard": kb
        }
    else:
        text += "✅ Ви безпечно дослідили територію"
        buttons = [[InlineKeyboardButton(text="🔙 Назад", callback_data="menu:main")]]
        kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    return text, kb

async def follow_tracks(user_id: int) -> Tuple[str, InlineKeyboardMarkup]:
    """Слідування за слідами"""
    if user_id not in ACTIVE_TRACKS:
        return "❌ Ви не знайшли слідів!", main_menu()
    
    tracks_data = ACTIVE_TRACKS[user_id]
    track = tracks_data["tracks"][0]  # Беремо перший слід
    
    if track["type"] == "enemy":
        # Зустріч з ворогом
        enemy = track["enemy"]
        text = (
            f"⚠️ Ви знайшли {enemy['name']}!\n\n"
            f"❤️ Ваше здоров'я: 100\n"  # TODO: Отримати з БД
            f"❤️ Здоров'я ворога: {enemy['hp']}\n"
            f"⚔️ Атака ворога: {enemy['attack']}\n"
            f"🛡 Захист ворога: {enemy['defense']}\n\n"
            "Оберіть дію:"
        )
        
        battle = {
            "enemy": enemy,
            "player_hp": 100,  # TODO: Отримати з БД
            "enemy_hp": enemy["hp"],
            "end_time": datetime.now() + timedelta(minutes=5),
            "keyboard": None
        }
        
        buttons = [
            [
                InlineKeyboardButton(text="⚔️ Атакувати", callback_data="hunt:attack"),
                InlineKeyboardButton(text="🛡 Захищатися", callback_data="hunt:defend")
            ],
            [
                InlineKeyboardButton(text="🏃 Втекти", callback_data="hunt:flee"),
                InlineKeyboardButton(text="🔙 Назад", callback_data="menu:main")
            ]
        ]
        kb = InlineKeyboardMarkup(inline_keyboard=buttons)
        battle["keyboard"] = kb
        ACTIVE_BATTLES[user_id] = battle
        del ACTIVE_TRACKS[user_id]
    else:
        # Зустріч з гравцем
        text = f"👤 Ви знайшли гравця! Він знаходиться в локації {track['location']}"
        buttons = [[InlineKeyboardButton(text="🔙 Назад", callback_data="menu:main")]]
        kb = InlineKeyboardMarkup(inline_keyboard=buttons)
        del ACTIVE_TRACKS[user_id]
    
    return text, kb

async def process_battle_action(user_id: int, action: str) -> str:
    """Обробка бойових дій"""
    if user_id not in ACTIVE_BATTLES:
        return "❌ Ви не в бою!"
    
    battle = ACTIVE_BATTLES[user_id]
    if datetime.now() >= battle["end_time"]:
        del ACTIVE_BATTLES[user_id]
        return "⏰ Час бою вийшов!"
    
    enemy = battle["enemy"]
    player_hp = battle["player_hp"]
    enemy_hp = battle["enemy_hp"]
    
    if action == "attack":
        # Атака гравця
        damage = calculate_final_dmg(15, enemy["defense"])  # TODO: Отримати атаку гравця з БД
        enemy_hp -= damage
        battle["enemy_hp"] = enemy_hp
        
        # Атака ворога
        if enemy_hp > 0:
            enemy_damage = calculate_final_dmg(enemy["attack"], 5)  # TODO: Отримати захист гравця з БД
            player_hp -= enemy_damage
            battle["player_hp"] = player_hp
            
            if player_hp <= 0:
                del ACTIVE_BATTLES[user_id]
                return "❌ Ви програли бій!"
        
        if enemy_hp <= 0:
            del ACTIVE_BATTLES[user_id]
            return f"✅ Ви перемогли {enemy['name']}!\n💰 Отримано: {enemy['gold']} золота\n✨ Досвід: {enemy['exp']}"
        
        return (
            f"⚔️ Ви завдали {damage} шкоди!\n"
            f"⚔️ Ворог завдав {enemy_damage} шкоди!\n\n"
            f"❤️ Ваше здоров'я: {player_hp}\n"
            f"❤️ Здоров'я ворога: {enemy_hp}"
        )
    
    elif action == "defend":
        # Захист гравця
        enemy_damage = calculate_final_dmg(enemy["attack"], 10)  # TODO: Отримати захист гравця з БД
        player_hp -= enemy_damage // 2  # Зменшуємо шкоду вдвічі
        battle["player_hp"] = player_hp
        
        if player_hp <= 0:
            del ACTIVE_BATTLES[user_id]
            return "❌ Ви програли бій!"
        
        return (
            f"🛡 Ви захищаєтесь!\n"
            f"⚔️ Ворог завдав {enemy_damage // 2} шкоди!\n\n"
            f"❤️ Ваше здоров'я: {player_hp}\n"
            f"❤️ Здоров'я ворога: {enemy_hp}"
        )
    
    elif action == "flee":
        # Спроба втечі
        if random.random() < 0.5:  # 50% шанс втечі
            del ACTIVE_BATTLES[user_id]
            return "🏃 Вам вдалося втекти!"
        else:
            enemy_damage = calculate_final_dmg(enemy["attack"], 5)
            player_hp -= enemy_damage
            battle["player_hp"] = player_hp
            
            if player_hp <= 0:
                del ACTIVE_BATTLES[user_id]
                return "❌ Ви програли бій!"
            
            return (
                f"❌ Втеча не вдалася!\n"
                f"⚔️ Ворог завдав {enemy_damage} шкоди!\n\n"
                f"❤️ Ваше здоров'я: {player_hp}\n"
                f"❤️ Здоров'я ворога: {enemy_hp}"
            )
    
    return "❌ Невідома дія" 