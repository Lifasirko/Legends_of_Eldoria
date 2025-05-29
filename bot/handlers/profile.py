from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from ..services.profile_service import get_profile_text, get_profile_keyboard

router = Router()

def register_handlers(dp):
    dp.include_router(router)

@router.message(Command("profile", "stats"))
async def cmd_profile(message: Message):
    text = await get_profile_text(message.from_user.id)
    kb = get_profile_keyboard()
    await message.answer(text, reply_markup=kb) 