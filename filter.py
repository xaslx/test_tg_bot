from aiogram.filters import Filter
from aiogram.types import Message
from dotenv import load_dotenv
import os


load_dotenv()
ADMIN_ID = os.getenv('ADMIN_ID')


class AdminProtect(Filter):

    def __init__(self):
        self.admins: int = ADMIN_ID

    async def __call__(self, message: Message):
        return message.from_user.id == int(self.admins)