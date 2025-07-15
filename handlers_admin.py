from aiogram import Router
from aiogram.types import Message, FSInputFile
from filter import AdminProtect
from aiogram.filters import Command, StateFilter
from pathlib import Path
from aiogram.fsm.state import default_state


router: Router = Router()


@router.message(AdminProtect(), Command('applications'), StateFilter(default_state))
async def get_applications(message: Message):
    file_path = Path('db/applications.csv')
    if not file_path.exists():
        await message.answer('Файл с заявками не найден.')
        return
    
    try:
        csv_file = FSInputFile(file_path, filename='applications.csv')
        await message.answer_document(
            document=csv_file,
            caption='📊 Все заявки пользователей'
        )
    except Exception as e:
        await message.answer(f'Ошибка при отправке файла, возможно он пустой')