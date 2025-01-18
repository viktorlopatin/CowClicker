from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types
from langs import f


def get_main_keyboard():
    builder = ReplyKeyboardBuilder()

    text = f("my cow button", "en")
    builder.add(types.KeyboardButton(text=text))

    return builder.as_markup(resize_keyboard=True)
