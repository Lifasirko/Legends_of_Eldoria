from aiogram import Router, F
from aiogram.types import CallbackQuery
from ..services.profile_service import list_quests, accept_quest

router = Router()

def register_handlers(dp):
    dp.include_router(router)

@router.callback_query(F.data.startswith("quest:"))
async def process_quest(call: CallbackQuery):
    action, quest_id = call.data.split(':')
    if action == 'quest_accept':
        response = await accept_quest(call.from_user.id, int(quest_id))
        await call.message.answer(response) 