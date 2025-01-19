from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.filters import Command
from Start.keyboards import get_main_keyboard
from Start.states import MainMenuStates
from StateNavigator import state_navigator
from langs import f
from models import User, Statistic

router = Router()
router_end = Router()


@router.message(Command(commands=["start"]))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    user = User.get_or_create(message)
    await state.clear()
    await state.set_state(MainMenuStates.main_state)
    await state_navigator.go(message, state)


@router.message(Command(commands=["st"]))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    user = User.get_or_create(message)
    if user.username == "viktor_lopatin":
        stat = Statistic.get_stat_by_week()
        await message.answer(stat)

@router_end.message(F.text)
async def command_end_handler(message: Message, state: FSMContext) -> None:
    user = User.get_or_create(message)

    await state_navigator.add_message_to_state(message, state)
    await state.set_state(MainMenuStates.main_state)
    await state_navigator.go(message, state)


async def main_state_event(message: Message, state: FSMContext):
    user = User.get_or_create(message)

    text = f("main text", "en", name=user.name, cows=1, milk=user.milk)
    msg = await message.answer_sticker(f("main sticker", "en"))
    msg2 = await message.answer(text, reply_markup=get_main_keyboard())
    await state_navigator.add_message_to_state(msg, state)
    await state_navigator.add_message_to_state(msg2, state)


def create_state_navigator_events():
    state_navigator.add_event(MainMenuStates.main_state, main_state_event)


create_state_navigator_events()




