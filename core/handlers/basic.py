from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from core.keyboards.replay import get_stat_keyboard
from core.db.db_request import Request
from core.utils.statesform import StepsForm



async def get_start(message: Message, state: FSMContext, request: Request):
    user = await request.get_user(message.from_user.id)
    if user is not None:
        await message.answer(f'С возвращением {message.from_user.first_name}!')
    else:
        await message.answer(
            f'Здравствуйте!\r\n'
            f'Рад помочь в учете Ваших расходов.\r\n'
            f'Подтверждаете согласие на обработку персональных данных? ↓',
            reply_markup=get_stat_keyboard()
        )
        await state.set_state(StepsForm.REGISTER)


async def register_user(message: Message, state: FSMContext, request: Request):
    if message.text == 'Да':
        await request.set_user(message.from_user.id, message.from_user.first_name)
        await message.answer(f'{message.from_user.first_name}, Спасибо за согласие')
        await state.clear()
    elif message.text == 'Нет':
        await message.answer(f'{message.from_user.first_name}, Возвращайтесь когда решите согласить,\r\n'
                             f'До свидания!')
        await state.clear()
    else:
        await message.answer(f'Выберите кнопку ↓', reply_markup=get_stat_keyboard())


async def get_cancel(message: Message, state: FSMContext):
    await message.answer(f'Действие отменно!', reply_markup=ReplyKeyboardRemove())
    await state.clear()


async def get_help(message: Message):
    await message.answer(
        f"Здравствуйте {message.from_user.first_name}, с помощью данного бота вы сможете контролировать свои расходы."
        f"\r\n\r\nДля успешной регистрации необходимо подтвердить согласие на обработку персональных данных."
        f"\r\nВоспользоваться командами из меню:"
        f"\r\n\r\n/my_expense - используйте для действий со своими расходами, вносить, получать, удалять, изменять "
        f"расходы загружать чеки в формате фото или документа, "
        f"получать статистику расходов за период или все внесенные расходы."
        f"\r\n\r\n/cancel - отменяет любое действие, если оно не завершено.", reply_markup=ReplyKeyboardRemove()
    )


async def empty_message(message: Message):
    await message.answer(f'{message.from_user.first_name}, Выберите кнопку в меню.')
    await message.delete()

# скрывает кнопку
# reply_markup=types.ReplyKeyboardRemove()
