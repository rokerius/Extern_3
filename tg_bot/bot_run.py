import asyncio

from aiogram import Bot, Dispatcher

from tg_bot.config import TOKEN
from app.handlers import router

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
    # @CU_extern_weather_bot
