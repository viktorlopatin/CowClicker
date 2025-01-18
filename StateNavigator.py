from aiogram.fsm.context import FSMContext
from aiogram.types import Message


class StateNavigator(object):
    """docstring for StateNavigator"""

    def __init__(self, ):
        super(StateNavigator, self).__init__()
        self.events = {}
        print("started")

    def add_event(self, current_state, event_func):
        print(current_state)
        self.events[current_state] = event_func

    async def go(self, message: Message, state: FSMContext):
        await self.delete_state_messages(state)
        await state.set_data({})
        await state.update_data({"message": message})
        current_state = await state.get_state()
        event_func = self.events[current_state]

        data = await state.get_data()
        await event_func(data["message"], state)

    async def add_message_to_state(self, msg: Message, state: FSMContext):
        msg_id = msg.message_id
        messages = await state.get_value("state_message")
        if not messages:
            await state.update_data({"state_message": []})
            messages = []
        messages.append(msg_id)
        await state.update_data({"state_message": messages})

        state_data = await state.get_value("state_message")
        print(state_data)

    async def delete_state_messages(self, state: FSMContext):
        messages_id = await state.get_value("state_message")
        if not messages_id:
            return
        message: Message = await state.get_value("message")
        for message_id in messages_id:
            try:
                await message.bot.delete_message(message.chat.id, message_id)
            except Exception as e:
                print(e)

        await state.update_data({"state_message": []})




state_navigator = StateNavigator()
