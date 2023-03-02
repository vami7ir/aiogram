from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_stat_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Да')
    keyboard_builder.button(text='Нет')
    keyboard_builder.adjust()
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True,
                                      input_field_placeholder='Выберите кнопку ↓')


def get_my_expense_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Внести расходы')
    keyboard_builder.button(text='Все расходы')
    keyboard_builder.button(text='Расходы за период')
    keyboard_builder.button(text='Загрузить чек')
    keyboard_builder.adjust()
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True,
                                      input_field_placeholder='Выберите кнопку ↓')
