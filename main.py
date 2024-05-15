from aiogram import executor
from config import admin_id, bot
import db

async def on_startup(dp):
    db.create_db()
    await bot.send_message(admin_id, "Бот запущен")

async def on_shutdown(dp):
    await bot.close()
    await bot.send_message(admin_id, "Бот выключен")

if __name__ == '__main__':
    from client import dp
    from admin import dp
    
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)