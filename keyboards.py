from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_currency_keyboard():
    """
    Создает клавиатуру с кнопками для бота
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Рубли в Доллары"), KeyboardButton(text="Доллары в Рубли")],
            [KeyboardButton(text="Текущий курс"), KeyboardButton(text="Помощь")]
        ],
        resize_keyboard=True
    )
    return keyboard