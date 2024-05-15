import os
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get('TOKEN') #hehe nice

bot = Bot(token=token, parse_mode='HTML')
memory_storage = MemoryStorage()
dp = Dispatcher(bot, storage=memory_storage)

admin_id = 471430149
batch_size = 100
channel_id = -1002016608492