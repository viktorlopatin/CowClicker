import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, F
from aiogram.client.default import DefaultBotProperties
from aiogram.types import PreCheckoutQuery, Message

from settings import TOKEN

from Start.start_handlers import router as start_router
from Start.start_handlers import router_end as router_end

from MyCows.handlers import router as my_cows_router

from langs import f


# ___ Bot Object ___
bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode='HTML'))


async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


# ___ Start Bot ___
async def main() -> None:
    dp = Dispatcher()
    dp.pre_checkout_query.register(pre_checkout_handler)

    dp.include_router(start_router)

    dp.include_router(my_cows_router)

    dp.include_router(router_end)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
