from config import batch_size, bot
from db import get_batch_users, create_batch_messages, set_batch_blocked, \
get_count_messages, get_batch_messages, delete_messages
from aiogram.utils.exceptions import BotBlocked
import asyncio

task_mailing = 0
task_delete_mailing = 0

async def mailing(data, users_count):
    for i in range(0, users_count, batch_size):
        users = get_batch_users(i, batch_size)
        messages_id, users_id = [], []
        blocked_ids = []
        for user in users:
            try:
                message = await bot.send_message(user[0], data['message']['text'], entities=data['message']['entities'], reply_markup=data['message']['reply_markup'])
                messages_id.append(message.message_id)
                users_id.append(message.chat.id)
            except BotBlocked:
                blocked_ids.append(user[0])
        create_batch_messages(messages_id, users_id)
        set_batch_blocked(blocked_ids)
    return 1

def create_task_mailing(data, users_count):
    global task_mailing
    task_mailing = asyncio.create_task(mailing(data, users_count[0][0])) # users_count[0][0] - unpacking array

def cancel_task_mailing():
    task_mailing.cancel()

async def delete_mailing():
    messages_count = get_count_messages()
    for i in range(0, messages_count[0][0], batch_size): # messages_count[0][0] - unpacking array
        data = get_batch_messages(i, batch_size)
        for message in data:
            try:
                await bot.delete_message(message[1], message[0])
            except Exception:
                pass
    delete_messages()
    return 1

def create_task_delete_mailing():
    global task_delete_mailing
    task_delete_mailing = asyncio.create_task(delete_mailing())