from aiogram import types
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from resources import texts
from resources import keyboards as kb
from config import admin_id, dp, bot
from states import Mailing, Channels
from db import create_channel, \
    get_count_users, get_count_messages, get_channels, delete_channel
import mailing
from mocks.mock_admin import *

@dp.message_handler(user_id=admin_id, commands=['admin'])
async def admin_handler(msg: Message):
    await msg.answer(texts.hello_admin, reply_markup=kb.reply_admin)

@dp.message_handler(lambda msg: msg.text == 'Создать рассылку' and msg.from_user.id == admin_id)
async def create_mailing_handler(msg: Message):
    await msg.answer('Создание рассылки, введите текст рассылки:')
    await Mailing.set_text.set()
    
@dp.message_handler(state=Mailing.set_text)
async def add_text_mailing_handler(msg: Message, state: FSMContext):
    await msg.answer(texts.mailing_text)
    await msg.answer(msg.text, entities=msg.entities, reply_markup=msg.reply_markup)
    await msg.answer(texts.mailing_choice, reply_markup=kb.inline_select_mailing)
    await state.update_data(message = msg)
    await state.reset_state(with_data=False)

@dp.callback_query_handler(lambda c: c.data == 'confirm', user_id = admin_id)
async def confirm_mailing_handler(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    users_count = get_count_users()
    mailing.create_task_mailing(data, users_count)
    if not mailing.task_mailing.done():
        await mailing.task_mailing
    await callback_query.message.answer('Рассылка завершена!')

@dp.callback_query_handler(lambda c: c.data == 'cancel', user_id = admin_id)
async def cancel_mailing_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await state.reset_state(True)
    try:
        if not mailing.task_mailing.done():
            mailing.cancel_task_mailing()
        mailing.create_task_delete_mailing()
        if not mailing.task_delete_mailing.done():
            await mailing.task_delete_mailing
    except Exception as e:
        print(e)
    await callback_query.message.answer('Рассылка отменена.')

@dp.message_handler(lambda msg: msg.text == 'Удалить рассылку' and msg.from_user.id == admin_id)
async def delete_mailing_handler(msg: Message):
    if get_count_messages()[0][0] == 0:
        await msg.answer('Рассылок нет!')
    else:
        if not mailing.task_mailing.done():
            mailing.cancel_task_mailing()
        mailing.create_task_delete_mailing()
        if not mailing.task_delete_mailing.done():
            await mailing.task_delete_mailing
        await msg.answer('Рассылка удалена!')

@dp.message_handler(lambda msg: msg.text == 'Добавить канал' and msg.from_user.id == admin_id)
async def add_channel_handler(msg: Message, state: FSMContext):
    await msg.answer('Напиши ссылку на канал')
    await state.set_state(Channels.set_link)

@dp.message_handler(state=Channels.set_link)
async def set_link_handler(msg: Message, state: FSMContext):
    link = msg.text
    await msg.answer('Напиши название канала')
    await state.update_data(link_data=link)
    await state.set_state(Channels.set_title)

@dp.message_handler(state=Channels.set_title)
async def set_title_handler(msg: Message, state: FSMContext):
    title = msg.text
    link = await state.get_data()
    create_channel(link['link_data'], title)
    await msg.answer('Готово! Канал добавлен!')
    await state.finish()

@dp.message_handler(lambda msg: msg.text == 'Удалить канал' and msg.from_user.id == admin_id)
async def delete_channel_handler(msg: Message):
    channels = get_channels()
    channels_markup = kb.create_markup(channels)
    await msg.answer('Выбери канал:', reply_markup=channels_markup)

@dp.callback_query_handler(lambda c: 'https://' in c.data, user_id = admin_id)
async def delete_channel_from_db_handler(callback_query: types.CallbackQuery):
    delete_channel(callback_query.data)
    await callback_query.message.answer('Готово! Канал удален!')

# @dp.my_chat_member_handler(lambda event: event.new_chat_member.status == 'administrator' or event.new_chat_member.status == 'left')
# async def bot_added_as_admin(event: ChatMemberUpdated):
#     if event.new_chat_member.status == 'administrator':
#         ref = await bot.create_chat_invite_link(event.chat.id, member_limit=1)
#         create_channel(ref.invite_link, event.chat.title)
#     if event.new_chat_member.status == 'left':
#         delete_channel_by_id(event.chat.id)