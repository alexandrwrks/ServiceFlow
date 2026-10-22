from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_keyboard():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Записаться", callback_data="sign_up")
    keyboard.button(text="Мои записи", callback_data="my_record")
    keyboard.button(text="Услуги", callback_data="services")
    keyboard.button(text="Помощь", callback_data="help")

    return keyboard.adjust(1).as_markup()
