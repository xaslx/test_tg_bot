from aiogram import Bot, Dispatcher
import asyncio
import os
import logging
from handlers import router
from handlers_admin import router as admin_router
from dotenv import load_dotenv
from aiogram.client.default import DefaultBotProperties


async def main() -> None:

    load_dotenv()
    
    token: str = os.getenv('TOKEN_BOT')
    bot: Bot = Bot(token=token, default=DefaultBotProperties(parse_mode='HTML'))
    dp: Dispatcher = Dispatcher()

    dp.include_router(admin_router)
    dp.include_router(router)
    



    await dp.start_polling(bot)
    
    
if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    asyncio.run(main())