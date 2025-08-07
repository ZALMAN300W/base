from aiogram import Router, F
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ChatMemberStatus
from create_bot import CHANNEL_ID, bot
from aiogram.enums import ChatMemberStatus
from aiogram.filters.command import Command
import logging




logger = logging.getLogger(__name__)
router = Router()


async def check_subscription(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]
    except Exception as e:
        logger.error(f"Ошибка проверки подписки: {e}")
        return False

@router.message(Command("bonus"))
async def message_handler(message: Message):
    user_id = message.from_user.id
    if await check_subscription(user_id):
        await message.answer("Вы подписаны на канал! Вот ваш бонус.\n https://docs.google.com/document/d/1Lu1ZILobD0p4RMDqpsouMjTMBIpIGoBTsFTUS9vV1ow/edit?usp=sharing")
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Подписаться на канал", url="https://t.me/elenafinplan")]
        ])
        await message.answer("Пожалуйста, подпишитесь на канал, чтобы продолжить!", reply_markup=keyboard)
