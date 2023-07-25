import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeAllGroupChats

from app_context import default_app_context
from routers import ROOT_ROUTER


async def main():
    async with default_app_context() as context:
        config = context.get_config()
        bot = Bot(token=config.tg_api_key, parse_mode=ParseMode.HTML)
        await bot.set_my_commands(
            commands=[
                BotCommand(command="start", description="Головне меню.")
            ],
            scope=BotCommandScopeAllGroupChats(),
        )
        dp = Dispatcher(storage=MemoryStorage())
        dp.include_router(ROOT_ROUTER)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
