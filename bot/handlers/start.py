from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from bot.keyboards.main_keyboard import main_menu
from bot.services.profile_service import get_profile_text, get_profile_keyboard
from bot.services.rest_service import rest
from bot.services.battle_service import quick_hunt, process_battle_action
from bot.services.quest_service import list_quests, accept_quest
import logging
import json

router = Router()
logger = logging.getLogger(__name__)

def log_callback(callback: CallbackQuery):
    """Логування callback даних"""
    logger.info(
        f"User {callback.from_user.id} pressed button: {callback.data}",
        extra={
            "user_id": callback.from_user.id,
            "username": callback.from_user.username,
            "callback_data": callback.data,
            "message_id": callback.message.message_id
        }
    )

def register_handlers(dp):
    dp.include_router(router)

@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обробник команди /start"""
    logger.info(f"User {message.from_user.id} started the bot")
    await message.answer(
        "Вітаю в грі! Оберіть дію:",
        reply_markup=main_menu()
    )

# Головне меню
@router.callback_query(F.data == "main_menu")
async def process_main_menu_callback(callback: CallbackQuery):
    """Обробник повернення в головне меню"""
    logger.info(f"User {callback.from_user.id} returned to main menu")
    await callback.message.edit_text(
        "Оберіть дію:",
        reply_markup=main_menu()
    )

# Профіль
@router.callback_query(F.data == "profile")
async def process_profile_callback(callback: CallbackQuery):
    """Обробник натискання кнопки профілю"""
    logger.info(f"User {callback.from_user.id} opened profile")
    profile_text = await get_profile_text(callback.from_user.id)
    keyboard = get_profile_keyboard()
    await callback.message.edit_text(
        profile_text,
        reply_markup=keyboard
    )

@router.callback_query(F.data == "profile:stats")
async def process_profile_stats(callback: CallbackQuery):
    log_callback(callback)
    text = await get_profile_text(callback.from_user.id)
    kb = get_profile_keyboard()
    if text != callback.message.text:
        await callback.message.edit_text(text, reply_markup=kb)
    else:
        await callback.answer("Статистика вже відображена")

@router.callback_query(F.data == "profile:inventory")
async def process_profile_inventory(callback: CallbackQuery):
    log_callback(callback)
    text = "🎒 Інвентар порожній"
    kb = get_profile_keyboard()
    if text != callback.message.text:
        await callback.message.edit_text(text, reply_markup=kb)
    else:
        await callback.answer("Інвентар вже відкритий")

# Відпочинок
@router.callback_query(F.data == "rest")
async def process_rest_callback(callback: CallbackQuery):
    """Обробник натискання кнопки відпочинку"""
    logger.info(f"User {callback.from_user.id} started rest")
    rest_text, keyboard = await rest(callback.from_user.id)
    await callback.message.edit_text(
        rest_text,
        reply_markup=keyboard
    )

# Полювання
@router.callback_query(F.data == "hunt")
async def process_hunt_callback(callback: CallbackQuery):
    """Обробник натискання кнопки полювання"""
    logger.info(f"User {callback.from_user.id} started hunting")
    hunt_text, keyboard = await quick_hunt(callback.from_user.id)
    await callback.message.edit_text(
        hunt_text,
        reply_markup=keyboard
    )

@router.callback_query(F.data.startswith("hunt:"))
async def process_hunt_action(callback: CallbackQuery):
    log_callback(callback)
    action = callback.data.split(":")[1]
    response = await process_battle_action(callback.from_user.id, action)
    if response != callback.message.text:
        await callback.message.edit_text(response, reply_markup=main_menu())
    else:
        await callback.answer("Дія вже виконана")

# Сліди
@router.callback_query(F.data.startswith("tracks:"))
async def process_tracks(callback: CallbackQuery):
    log_callback(callback)
    action = callback.data.split(":")[1]
    if action == "follow":
        text, kb = await follow_tracks(callback.from_user.id)
        await callback.message.edit_text(text, reply_markup=kb)
    else:
        await callback.answer("Невідома дія")

# Квести
@router.callback_query(F.data == "quests")
async def process_quests_callback(callback: CallbackQuery):
    log_callback(callback)
    text = await list_quests(callback.from_user.id)
    if text != callback.message.text:
        await callback.message.edit_text(text, reply_markup=main_menu())
    else:
        await callback.answer("Список квестів вже відкритий")

@router.callback_query(F.data.startswith("quest:"))
async def process_quest_action(callback: CallbackQuery):
    log_callback(callback)
    action, quest_id = callback.data.split(":")
    if action == "quest_accept":
        response = await accept_quest(callback.from_user.id, int(quest_id))
        if response != callback.message.text:
            await callback.message.edit_text(response, reply_markup=main_menu())
        else:
            await callback.answer("Квест вже прийнято") 