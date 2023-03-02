from aiogram import Dispatcher, F, Bot
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_di import ContextSchedulerDecorator

from core.db.db_request import Request
from core.handlers.basic import get_start, register_user, get_help, get_cancel, empty_message
from core.handlers.expenses import my_expense, set_expense, get_expense, state_expense, get_expense_period, \
    set_check_expense_document, set_check_expense_photo, set_expense_check
from core.settings import settings
from core.utils.commands import set_commands
from core.middlewares.apschedulermiddleware import SchedulerMiddleware
from core.middlewares.dbmiddleware import DbSession
from core.db.db_connect import postgres_connect
from core.utils.logged import log
from core.utils.redis_connect import redis_connect_storage, redis_connect_jobstores
from core.utils.statesform import StepsForm
from core.handlers.apsched import send_expense_mouth

import asyncio


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Бот запущен!', reply_markup=ReplyKeyboardRemove())


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот остановлен!', reply_markup=ReplyKeyboardRemove())


async def statr():
    log()
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    poll_connect = await postgres_connect()
    request = Request(poll_connect)

    dp = Dispatcher(storage=redis_connect_storage())
    scheduler = ContextSchedulerDecorator(
        AsyncIOScheduler(timezone="Europe/Moscow", jobstores=redis_connect_jobstores())
    )
    scheduler.ctx.add_instance(bot, declared_class=Bot)
    scheduler.ctx.add_instance(request, declared_class=Request)
    scheduler.add_job(send_expense_mouth, trigger='cron', day='1', hour=10, minute=00)
    scheduler.start()

    dp.update.middleware.register(DbSession(poll_connect))
    dp.update.middleware.register(SchedulerMiddleware(scheduler))

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(get_cancel, Command(commands='cancel'))
    dp.message.register(get_help, Command(commands='help'))

    dp.message.register(set_expense_check, F.text == 'Загрузить чек')
    dp.message.register(get_expense, F.text == 'Все расходы')
    dp.message.register(get_expense_period, StepsForm.GET_EXPENSE_PERIOD)
    dp.message.register(set_expense, StepsForm.SET_EXPENSE)
    dp.message.register(state_expense, StepsForm.EXPENSE)
    dp.message.register(set_check_expense_photo, StepsForm.SET_EXPENSE_CHECK and F.photo)
    dp.message.register(set_check_expense_document, StepsForm.SET_EXPENSE_CHECK and F.document)
    dp.message.register(my_expense, Command(commands='my_expense'))

    dp.message.register(get_start, Command(commands='start'))
    dp.message.register(register_user, StepsForm.REGISTER)
    dp.message.register(empty_message)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(statr())
