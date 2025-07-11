from aiogram.fsm.state import StatesGroup, State

class House(StatesGroup):

    start = State()
    house_type = State()
    show_examples = State()
    confirm_after_examples = State()
    confirm_brick = State()
    confirm_frame = State()
    confirm_modular = State()
    confirm_undefined = State()
    select_area = State()
    select_plot = State()
    select_budget = State()
    select_timing = State()
    comment = State()
    phone = State()
    name = State()
    finish = State()
