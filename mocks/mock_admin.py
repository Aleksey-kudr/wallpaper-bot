from config import dp, admin_id
from aiogram.types import Message
from db import create_test_user, create_test_message, get_count_users, get_count_messages, con, get_count_channels

# fil db mock users
@dp.message_handler(user_id = admin_id, commands=['fill_users_table'])
async def test_users(msg: Message):
    for i in range(100):
        create_test_user(i)
    con.commit()
    await msg.answer('Готово')

# fill db mock messages
@dp.message_handler(user_id = admin_id, commands=['fill_messages_table'])
async def test_messages(msg: Message):
    for i in range(10000):
        create_test_message(i)
    con.commit()
    await msg.answer('Готово')

# get count of users and messages
@dp.message_handler(user_id = admin_id, commands=['get_count'])
async def test_count(msg: Message):
    await msg.answer(f'users: {get_count_users()[0][0]}, messages: {get_count_messages()[0][0]}, channels: {get_count_channels()[0][0]}')