from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
)


def start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text='🔘 Начать', callback_data='start')
        ]]
    )


def house_type_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🔘 Кирпичный', callback_data='type_brick'),
                InlineKeyboardButton(text='🔘 Каркасный', callback_data='type_frame'),
            ],
            [
                InlineKeyboardButton(text='🔘 Модульный', callback_data='type_modular'),
                InlineKeyboardButton(text='🔘 Ещё не определился', callback_data='type_unknown'),
            ],
            [
                InlineKeyboardButton(text='📸 Примеры работ', callback_data='examples')
            ]
        ]
    )


def examples_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🔘 Да', callback_data='continue_after_examples')],
            [InlineKeyboardButton(text='🔘 Выйти', callback_data='exit')],
        ]
    )


def confirm_type_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🔘 Да', callback_data='next_area')],
            [InlineKeyboardButton(text='🔘 Выйти', callback_data='back_to_type')],
        ],
    )

def area_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=area, callback_data=f'area_{i}')]
        for i, area in enumerate([
            'до 100 м²', '100–150 м²', '150–200 м²', 'более 200 м²', 'Пока не знаю'
        ])
    ]
    buttons.append([InlineKeyboardButton(text='🏠 Главное меню', callback_data='main_menu')])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def plot_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text=plot, callback_data=f'plot_{i}')
        ] for i, plot in enumerate([
            'Да', 'В процессе покупки', 'Пока нет', 'Нужна помощь с подбором'
        ])]
    )


def budget_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text=budget, callback_data=f'budget_{i}')
        ] for i, budget in enumerate([
            'до 3 млн ₽', '3–5 млн ₽', '5–8 млн ₽', 'более 8 млн ₽', 'Пока не решил(а)'
        ])]
    )


def time_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text=timing, callback_data=f'timing_{i}')
        ] for i, timing in enumerate([
            'В ближайшие 1–2 месяца', 'Через 3–6 месяцев', 'Через год', 'Просто интересуюсь'
        ])]
    )


def comment_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🔘 Пропустить', callback_data='skip_comment')],
            [InlineKeyboardButton(text='🏠 Главное меню', callback_data='main_menu')]
        ]
    )