from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from Start.keyboards import get_main_keyboard
from MyCows.states import MyCowsMenuStates
from StateNavigator import state_navigator
from MyCows.keyboards import back_keyboard
from models import User
from langs import f


async def my_cows_menu(message: Message, state: FSMContext):
    user = User.get_or_create(message)

    status, del_time, keyboard = user.get_cow_status()
    print(status, del_time)
    params = {"text": f(f"text step {status}", "en"),
              "reply_markup": keyboard}
    if status == 2:
        params["text"] = f(f"text step {status}", "en", time_remaining=del_time)

    msg = await message.answer_sticker(f(f"cow step {status}", "en"), reply_markup=back_keyboard())
    msg2 = await message.answer(**params)

    await state_navigator.add_message_to_state(msg, state)
    await state_navigator.add_message_to_state(msg2, state)


def create_state_navigator_events():
    state_navigator.add_event(MyCowsMenuStates.main_state, my_cows_menu)


create_state_navigator_events()