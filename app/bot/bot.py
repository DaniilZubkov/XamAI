from aiogram import types
from aiogram.types import Message
from aiogram import Router, F
from aiogram.filters import CommandStart
import logging

from database.conn import db
from nlp.generate import create_response

logger = logging.getLogger(__name__)
router = Router()

@router.message(CommandStart())
async def handle_start_message(message: Message):
    try:
        user_data = {
            'telegram_user_id': message.from_user.id,
            'username': message.from_user.username,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'language_code': message.from_user.language_code,
            'is_bot': message.from_user.is_bot,
            'is_premium': getattr(message.from_user, 'is_premium', False),
            'signup_source': 'telegram'
        }

        user_id = await db.register_user(user_data)
        
        # LOGIC HERE
        if user_id:
            await message.answer(f"Привет, {message.from_user.first_name}, я хамло еще то!\n\n"
                                 f"***Я буду хамить тебе когда ты отправишь мне сообение, но только не обижайся ;)***", parse_mode="MARKDOWN")
        else:
            await message.answer(f"Привет, {message.from_user.first_name}, я хамло еще то!\n\n"
                                 f"***Я буду хамить тебе когда ты отправишь мне сообение, но только не обижайся ;)***", parse_mode="MARKDOWN")

    except Exception as e:
        logger.error(f"Error in handle_start_message: {e}", exc_info=True)







@router.message()
async def handle_message(message: Message):
    try:
        enable_message = await message.answer("⏳***Подожди, готовлю оскорбление для тебя...***", parse_mode="MARKDOWN")
        text = message.text

        response = await create_response(text)

        await enable_message.delete()
        await message.answer(response, parse_mode="MARKDOWN")
    except Exception as e:
        print(e)
