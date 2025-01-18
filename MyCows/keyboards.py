from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram import types
from langs import f


def back_keyboard():
    builder = ReplyKeyboardBuilder()

    text = "⬅️ Back"
    builder.add(types.KeyboardButton(text=text))

    return builder.as_markup(resize_keyboard=True)


def step_1_keyboard():
    builder = InlineKeyboardBuilder()

    text = f("send cow button", "en")
    callback_data = "send cow"

    builder.add(types.InlineKeyboardButton(text=text, callback_data=callback_data))
    return builder.as_markup()


def step_2_keyboard():
    builder = InlineKeyboardBuilder()

    text = f("update button", "en")
    callback_data = "update button"

    builder.add(types.InlineKeyboardButton(text=text, callback_data=callback_data))

    text2 = f("premium button", "en")
    callback_data2 = "premium button"

    builder.row(types.InlineKeyboardButton(text=text2, callback_data=callback_data2))
    return builder.as_markup()


def step_3_keyboard():
    builder = InlineKeyboardBuilder()

    text = f("collect milk", "en")
    callback_data = "collect milk"

    builder.add(types.InlineKeyboardButton(text=text, callback_data=callback_data))
    return builder.as_markup()


def payment_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Pay 10 ⭐️", pay=True)

    return builder.as_markup()
