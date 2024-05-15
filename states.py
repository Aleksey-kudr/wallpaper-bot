from aiogram.dispatcher.filters.state import StatesGroup, State

class Mailing(StatesGroup):
    set_text = State()

class Channels(StatesGroup):
    set_link = State()
    set_title = State()