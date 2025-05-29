from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from ..services.battle_service import quick_hunt

router = Router()

def register_handlers(dp):
    dp.include_router(router)

@router.message(Command("hunt", "explore"))
async def cmd_hunt(message: Message):
    text, kb = await quick_hunt(message.from_user.id)
    await message.answer(text, reply_markup=kb) 