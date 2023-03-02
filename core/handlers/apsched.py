from datetime import datetime

from aiogram import Bot
from dateutil.relativedelta import relativedelta

from core.db.db_request import Request


async def send_expense_mouth(bot: Bot, request: Request):
    date_now = str(datetime.now())
    date_one_month = str(datetime.now() - relativedelta(months=1))
    period = [date_one_month, date_now]
    users = await request.get_users_all()
    for user in users:
        summ = await request.get_expense_period(user['telegram_id'], period)
        await bot.send_message(user['telegram_id'], f"За прошлый месяц, расходы составили {summ} руб.")
