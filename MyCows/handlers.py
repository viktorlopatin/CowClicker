from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, LabeledPrice
from Start.states import MainMenuStates
from MyCows.states import MyCowsMenuStates
from StateNavigator import state_navigator
from models import User
from langs import f
from MyCows.keyboards import payment_keyboard

from MyCows import menu_event

router = Router()


@router.message(lambda c: c.text == "My Cow 🐮", MainMenuStates.main_state)
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(MyCowsMenuStates.main_state)
    await state_navigator.add_message_to_state(message, state)
    await state_navigator.go(message, state)


@router.message(lambda c: c.text == "⬅️ Back", MyCowsMenuStates.main_state)
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state_navigator.add_message_to_state(message, state)
    await state.set_state(MainMenuStates.main_state)
    await state_navigator.go(message, state)


@router.callback_query(lambda c: c.data == "send cow")
async def send_cow_button_handler(query: types.CallbackQuery, state: FSMContext) -> None:
    user = User.get_or_create(query.message)
    user.send_cow()
    await state_navigator.go(query.message, state)


@router.callback_query(lambda c: c.data == "update button")
async def update_cow_button_handler(query: types.CallbackQuery, state: FSMContext) -> None:
    user = User.get_or_create(query.message)
    status, del_time, keyboard = user.get_cow_status()
    if status == 2:
        text = f(f"text step {status}", "en", time_remaining=del_time)
        await query.message.edit_text(text, reply_markup=keyboard)
    else:
        await state_navigator.go(query.message, state)


@router.callback_query(lambda c: c.data == "premium button")
async def premium_cow_button_handler(query: types.CallbackQuery, state: FSMContext) -> None:
    prices = [LabeledPrice(label="XTR", amount=1)]
    msg = await query.message.answer_invoice(
        title="Collect Milk Now",
        description="Collect milk now for 10 Start",
        prices=prices,
        provider_token="",
        payload="channel_support",
        currency="XTR",
        reply_markup=payment_keyboard(),

    )

    await state_navigator.add_message_to_state(msg, state)


@router.message(F.successful_payment)
async def success_payment_handler(message: Message, state: FSMContext):
    user = User.get_or_create(message)
    user.set_premium_cow()
    await state_navigator.go(message, state)


@router.callback_query(lambda c: c.data == "collect milk")
async def collect_cow_button_handler(query: types.CallbackQuery, state: FSMContext) -> None:
    user = User.get_or_create(query.message)
    user.collect_milk()
    await query.answer(f("get milk answer", "en"), show_alert=True)
    await state_navigator.go(query.message, state)
