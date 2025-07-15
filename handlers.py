from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from states import House
from keyboards import (
    area_keyboard, plot_keyboard, time_keyboard,
    start_keyboard, budget_keyboard, comment_keyboard,
    examples_keyboard, house_type_keyboard, confirm_type_keyboard
)
from aiogram.fsm.state import default_state
from text import frame_text, brick_text, modular_text, unknown_text, menu_text, BUDGET_MAPPING, PLOT_MAPPING, TIMING_MAPPING
import os
from dotenv import load_dotenv
from utils import save_application


load_dotenv()

router: Router = Router()
ADMIN_ID: int = os.getenv('ADMIN_ID')
token = os.getenv('TOKEN_BOT')
bot: Bot = Bot(token=token)


@router.callback_query(F.data == 'main_menu')
async def main_menu(callback: CallbackQuery, state: FSMContext):
    text = menu_text()
    await callback.message.edit_text(
        text=text,
        reply_markup=house_type_keyboard(),
    )
    await state.set_state(House.house_type)


@router.message(CommandStart(), StateFilter(default_state))
async def start_bot(message: Message, state: FSMContext):
    await message.answer(
        text=('📌 Продолжая отвечать на вопросы бота, вы <a href="https://site-it.su/"><b>соглашаетесь на\n'
              'обработку персональных данных</b></a> согласно политике конфиденциальности.'),
        reply_markup=start_keyboard(),
        disable_web_page_preview=True,
    )
    await state.set_state(House.start)


@router.callback_query(F.data == 'start', StateFilter(House.start))
async def on_start_pressed(callback: CallbackQuery, state: FSMContext):
    text = menu_text()
    await callback.message.edit_text(
        text=text,
        reply_markup=house_type_keyboard(),
    )
    await state.set_state(House.house_type)


@router.callback_query(F.data == 'examples', StateFilter(House.house_type))
async def get_examples(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        '📸 Вот примеры наших реализованных проектов:\n'
        '👉 <a href="https://site-it.su/">Посмотреть</a>\n\nПродолжим подбор?',
        reply_markup=examples_keyboard(),
    )
    await state.set_state(House.show_examples)


@router.callback_query(F.data == 'continue_after_examples', StateFilter(House.show_examples))
async def back_to_type(callback: CallbackQuery, state: FSMContext):
    text = menu_text()
    await callback.message.edit_text(
        text=text,
        reply_markup=house_type_keyboard(),
    )
    await state.set_state(House.house_type)


@router.callback_query(F.data == 'exit')
async def exit_flow(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('❌ Диалог завершён. Чтобы начать заново, напишите /start')
    await state.clear()


@router.callback_query(F.data == 'type_brick', StateFilter(House.house_type))
async def handle_brick(callback: CallbackQuery, state: FSMContext):
    text = brick_text()
    await state.update_data(house_type_ru="Кирпичный")
    await callback.message.edit_text(text, reply_markup=confirm_type_keyboard())
    await state.set_state(House.confirm_brick)


@router.callback_query(F.data == 'type_frame', StateFilter(House.house_type))
async def handle_frame(callback: CallbackQuery, state: FSMContext):
    text = frame_text()
    await state.update_data(house_type_ru='Каркасный')
    await callback.message.edit_text(text, reply_markup=confirm_type_keyboard())
    await state.set_state(House.confirm_frame)


@router.callback_query(F.data == 'type_modular', StateFilter(House.house_type))
async def handle_modular(callback: CallbackQuery, state: FSMContext):
    text = modular_text()
    await state.update_data(house_type_ru='Модульный')
    await callback.message.edit_text(text, reply_markup=confirm_type_keyboard())
    await state.set_state(House.confirm_modular)


@router.callback_query(F.data == 'type_unknown', StateFilter(House.house_type))
async def handle_unknown(callback: CallbackQuery, state: FSMContext):
    text = unknown_text()
    await state.update_data(house_type_ru='Неизвестный тип')
    await callback.message.edit_text(text, reply_markup=confirm_type_keyboard())
    await state.set_state(House.confirm_undefined)


@router.callback_query(F.data == 'next_area', StateFilter(House.confirm_brick, House.confirm_frame, House.confirm_modular, House.confirm_undefined))
async def go_to_area(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Примерная площадь дома:', reply_markup=area_keyboard())
    await state.set_state(House.select_area)


@router.callback_query(F.data == 'back_to_type', StateFilter(House.confirm_brick, House.confirm_frame, House.confirm_modular, House.confirm_undefined))
async def go_back_type(callback: CallbackQuery, state: FSMContext):
    text = menu_text()
    await callback.message.edit_text(
        text=text,
        reply_markup=house_type_keyboard(),
    )
    await state.set_state(House.house_type)


@router.callback_query(StateFilter(House.select_area))
async def set_area(callback: CallbackQuery, state: FSMContext):
    await state.update_data(area=callback.data)
    await callback.message.edit_text(
        'У вас уже есть участок под строительство?',
        reply_markup=plot_keyboard()
    )
    await state.set_state(House.select_plot)

@router.callback_query(StateFilter(House.select_plot))
async def set_plot(callback: CallbackQuery, state: FSMContext):
    plot_value = PLOT_MAPPING.get(callback.data, callback.data)
    await state.update_data(
        plot=callback.data,
        plot_ru=plot_value
    )
    await callback.message.edit_text(
        'Какой ориентировочный бюджет?',
        reply_markup=budget_keyboard()
    )
    await state.set_state(House.select_budget)

@router.callback_query(StateFilter(House.select_budget))
async def set_budget(callback: CallbackQuery, state: FSMContext):
    budget_value = BUDGET_MAPPING.get(callback.data, callback.data)
    await state.update_data(
        budget=callback.data,
        budget_ru=budget_value
    )
    await callback.message.edit_text(
        'Когда планируете начать строительство?',
        reply_markup=time_keyboard()
    )
    await state.set_state(House.select_timing)


@router.callback_query(StateFilter(House.select_timing))
async def set_timing(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    timing_value = TIMING_MAPPING.get(callback.data, callback.data)
    await state.update_data(
        timing=callback.data,
        timing_ru=timing_value
    )
    

    await callback.message.edit_text(
        'Хотите оставить комментарий, пожелания или вопрос?\n(Можно пропустить)',
        reply_markup=comment_keyboard()
    )

    await state.set_state(House.comment)


@router.callback_query(F.data == 'skip_comment', StateFilter(House.comment))
async def skip_comment(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        '📱 Введите номер телефона в формате 79991234567',
    )
    await state.set_state(House.phone)


@router.message(StateFilter(House.comment), F.text)
async def save_comment(message: Message, state: FSMContext):
    data = await state.get_data()
    comment_msg_id = data.get('comment_msg_id')

    try:
        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=comment_msg_id
        )
    except:
        pass
    
    await message.answer(
        '📱 Введите номер телефона в формате 79991234567',
    )
    
    await state.update_data(comment=message.text)
    await state.set_state(House.phone)


@router.message(StateFilter(House.phone))
async def handle_phone_input(message: Message, state: FSMContext):
    phone = message.text.strip()
    
    if not phone.isdigit():
        await message.answer('❌ Номер должен содержать только цифры. Пример: 79991234567')
        return
    
    if len(phone) != 11:
        await message.answer('❌ Номер должен содержать 11 цифр. Пример: 79991234567')
        return
    
    if not phone.startswith(('7', '8')):
        await message.answer('❌ Номер должен начинаться с 7 или 8. Пример: 79991234567')
        return
    
    await state.update_data(phone=phone)
    await message.answer('🧑 Как вас зовут?')
    await state.set_state(House.name)


@router.message(F.contact, StateFilter(House.phone))
async def handle_contact(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await message.answer('🧑 Как вас зовут?', reply_markup=ReplyKeyboardRemove())
    await state.set_state(House.name)


@router.message(F.text, StateFilter(House.name))
async def set_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    await message.answer(
        f'Спасибо, {data.get('name')}! Мы получили вашу заявку.\n'
        'Наш специалист свяжется с вами в ближайшее время 📞\n\n'
        '📸 Пока можно посмотреть ещё примеры работ:\n'
        '👉 <a href="https://site-it.su/">Перейти на сайт</a>',
        reply_markup=ReplyKeyboardRemove(),
    )
    
    response = (
        '🏠 Новая заявка на строительство\n\n'
        f'▪ Имя: {data.get('name', 'не указано')}\n'
        f'▪ Телефон: {data.get('phone', 'не указан')}\n'
        f'▪ Тип дома: {data.get('house_type_ru', 'не указан')}\n'
        f'▪ Участок: {data.get('plot_ru', 'не указан')}\n'
        f'▪ Бюджет: {data.get('budget_ru', 'не указан')}\n'
        f'▪ Сроки строительства: {data.get('timing_ru', 'не указаны')}\n'
        f'▪ Комментарий: {data.get('comment', 'не указан')}'
    )

    save_application(data=data)
    await bot.send_message(chat_id=int(ADMIN_ID), text=response)
    await state.clear()


@router.message(StateFilter(default_state))
async def echo(message: Message):
    await message.answer(
        'Чтобы начать, введите команду /start'
    )