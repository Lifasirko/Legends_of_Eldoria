from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from ..services.rest_service import rest

router = Router()

def register_handlers(dp):
    dp.include_router(router)

@router.message(Command("rest"))
async def cmd_rest(message: Message):
    # Очікуємо формат "/rest 1h30m" або "/rest"
    args = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
    response = await rest(message.from_user.id, args)
    await message.answer(response) 