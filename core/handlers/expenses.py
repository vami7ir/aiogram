import re
import os

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram import Bot

from core.keyboards.replay import get_my_expense_keyboard
from core.utils.statesform import StepsForm
from core.db.db_request import Request


async def my_expense(message: Message, state: FSMContext) -> None:
    await message.answer(f'{message.from_user.first_name}, Выберите кнопку ↓',
                         reply_markup=get_my_expense_keyboard())
    await state.set_state(StepsForm.EXPENSE)


async def state_expense(message: Message, state: FSMContext) -> None:
    if message.text == 'Внести расходы':
        await message.answer(f'{message.from_user.first_name}, Введите сумму затрат.')
        await state.set_state(StepsForm.SET_EXPENSE)
    elif message.text == 'Расходы за период':
        await message.answer(f'Введите диапазон даты в формате. (0000-00-00 0000-00-00)')
        await state.set_state(StepsForm.GET_EXPENSE_PERIOD)
    else:
        await my_expense(message, state)
        await state.clear()


async def set_expense(message: Message, state: FSMContext, request: Request) -> None:
    try:
        summ = float(message.text)
        await request.set_expense(message.from_user.id, summ)
        await message.answer(
            f'{message.from_user.first_name}, '
            f'Сумма внесена.', reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
    except ValueError:
        await message.answer(
            f'{message.from_user.first_name}, Введите сумму затрат, а не текст',
            reply_markup=ReplyKeyboardRemove()
        )


async def get_expense(message: Message, state: FSMContext, request: Request) -> None:
    summ = await request.get_expense(message.from_user.id)
    await message.answer(f"Все ваши расходы {summ} руб.", reply_markup=ReplyKeyboardRemove())
    await state.clear()


async def get_expense_period(message: Message, state: FSMContext, request: Request) -> None:
    period = re.findall(r'\d{4}-\d{2}-\d{2}', message.text)
    if len(period) == 2:
        summ = await request.get_expense_period(message.from_user.id, period)
        await message.answer(f"За период {message.text}, расходы составили {summ} руб.",
                             reply_markup=ReplyKeyboardRemove())
        await state.clear()
    else:
        await message.answer(f'Введите диапазон даты в формате. (0000-00-00 0000-00-00)')


# check_expense

async def set_expense_check(message: Message, state: FSMContext):
    await message.answer(f'Загрузите фото или документ.')
    await state.set_state(StepsForm.SET_EXPENSE_CHECK)


async def set_check_expense_document(message: Message, bot: Bot, state: FSMContext, request: Request):
    file = await bot.get_file(message.document.file_id)
    path = f'file/document/{message.from_user.id}'
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    file_path = f'{path}/{message.document.file_id}.jpg'
    await bot.download_file(file.file_path, file_path)
    await request.set_document(message.from_user.id, file_path)
    await message.answer(f'Получил документ')
    await state.clear()


async def set_check_expense_photo(message: Message, bot: Bot, state: FSMContext, request: Request):
    file = await bot.get_file(message.photo[-1].file_id)
    path = f'file/photo/{message.from_user.id}'
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    file_path = f'{path}/{message.photo[-1].file_id}.jpg'
    await bot.download_file(file.file_path, file_path)
    await request.set_photo(message.from_user.id, file_path)
    await message.answer(f'Получил фотографию')
    await state.clear()
