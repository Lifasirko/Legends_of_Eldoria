from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from ..keyboards.main_keyboard import main_menu
from ..services.profile_service import get_profile_text, get_profile_keyboard
from ..services.rest_service import rest
from ..services.battle_service import quick_hunt, process_battle_action
from ..services.quest_service import list_quests, accept_quest
import logging

router = Router()
logger = logging.getLogger(__name__)

def register_handlers(dp):
    dp.include_router(router)

@router.message(Command("start"))
async def cmd_start(message: Message):
    logger.info(f"User {message.from_user.id} started the bot")
    await message.answer(
        "🏰 Легенди Ельдорії\nВітаю, Герою! Обери дію:",
        reply_markup=main_menu()
    )

# Головне меню
@router.callback_query(F.data == "menu:main")
async def process_main_menu(callback: CallbackQuery):
    logger.info(f"User {callback.from_user.id} returned to main menu")
    await callback.message.edit_text(
        "🏰 Легенди Ельдорії\nВітаю, Герою! Обери дію:",
        reply_markup=main_menu()
    )

# Профіль
@router.callback_query(F.data == "profile")
async def process_profile_callback(callback: CallbackQuery):
    logger.info(f"User {callback.from_user.id} opened profile")
    text = await get_profile_text(callback.from_user.id)
    kb = get_profile_keyboard()
    if text != callback.message.text:
        await callback.message.edit_text(text, reply_markup=kb)
    else:
        await callback.answer("Профіль вже відкритий")

@router.callback_query(F.data == "profile:stats")
async def process_profile_stats(callback: CallbackQuery):
    logger.info(f"User {callback.from_user.id} viewed stats")
    text = await get_profile_text(callback.from_user.id)
    kb = get_profile_keyboard()
    if text != callback.message.text:
        await callback.message.edit_text(text, reply_markup=kb)
    else:
        await callback.answer("Статистика вже відображена")

@router.callback_query(F.data == "profile:inventory")
async def process_profile_inventory(callback: CallbackQuery):
    logger.info(f"User {callback.from_user.id} opened inventory")
    text = "🎒 Інвентар порожній"
    kb = get_profile_keyboard()
    if text != callback.message.text:
        await callback.message.edit_text(text, reply_markup=kb)
    else:
        await callback.answer("Інвентар вже відкритий")

# Відпочинок
@router.callback_query(F.data == "rest")
async def process_rest_callback(callback: CallbackQuery):
    logger.info(f"User {callback.from_user.id} started resting")
    response = await rest(callback.from_user.id, "1h")  # За замовчуванням 1 година
    if response != callback.message.text:
        await callback.message.edit_text(response, reply_markup=main_menu())
    else:
        await callback.answer("Ви вже відпочиваєте")

# Полювання
@router.callback_query(F.data == "hunt")
async def process_hunt_callback(callback: CallbackQuery):
    logger.info(f"User {callback.from_user.id} started hunting")
    text, kb = await quick_hunt(callback.from_user.id)
    if text != callback.message.text:
        await callback.message.edit_text(text, reply_markup=kb)
    else:
        await callback.answer("Ви вже в бою")

@router.callback_query(F.data.startswith("hunt:"))
async def process_hunt_action(callback: CallbackQuery):
    action = callback.data.split(":")[1]
    logger.info(f"User {callback.from_user.id} performed action: {action}")
    response = await process_battle_action(callback.from_user.id, action)
    if response != callback.message.text:
        await callback.message.edit_text(response, reply_markup=main_menu())
    else:
        await callback.answer("Дія вже виконана")

# Квести
@router.callback_query(F.data == "quests")
async def process_quests_callback(callback: CallbackQuery):
    logger.info(f"User {callback.from_user.id} opened quests")
    text = await list_quests(callback.from_user.id)
    if text != callback.message.text:
        await callback.message.edit_text(text, reply_markup=main_menu())
    else:
        await callback.answer("Список квестів вже відкритий")

@router.callback_query(F.data.startswith("quest:"))
async def process_quest_action(callback: CallbackQuery):
    action, quest_id = callback.data.split(":")
    logger.info(f"User {callback.from_user.id} performed quest action: {action} for quest {quest_id}")
    if action == "quest_accept":
        response = await accept_quest(callback.from_user.id, int(quest_id))
        if response != callback.message.text:
            await callback.message.edit_text(response, reply_markup=main_menu())
        else:
            await callback.answer("Квест вже прийнято") 