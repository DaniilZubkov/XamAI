import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from aiogram import Bot, Dispatcher
import asyncio
import logging

from config.settings import TELEGRAM_TOKEN, DB_CONFIG
from app.bot.bot import router
from database.conn import db



bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

async def on_startup():
    await db.create_pool(**DB_CONFIG)
    logging.info("Bot started")

async def on_shutdown():
    await db.close()
    logging.info("Bot stopped")







async def main():
    dp.include_router(router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        await bot.session.close()

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    asyncio.run(main())
