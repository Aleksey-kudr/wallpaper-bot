import asyncio
from aiogram import types
from aiogram.types import Message, ContentType
import random
from config import bot, dp, channel_id
from db import create_user, get_channels
from resources import texts
from resources import keyboards as kb

@dp.message_handler(commands=['start'])
async def start_handler(msg: Message):
    create_user(msg.from_user.id)    
    await msg.answer(texts.hello, reply_markup=kb.inline_start)

@dp.callback_query_handler(lambda c: c.data == 'start')
async def process_callback_start(callback_query: types.CallbackQuery):
    await callback_query.message.answer(texts.start_answer)

@dp.message_handler(content_types=ContentType.PHOTO)
async def photo_handler(msg: Message):
    await msg.answer(texts.good)
    await msg.answer(texts.loading)
    await asyncio.sleep(3)
    await msg.answer(texts.analysis)
    await asyncio.sleep(3)
    await msg.answer(texts.setsize)
    await asyncio.sleep(3)
    await msg.answer(texts.success, reply_markup=kb.inline_select_money)

@dp.callback_query_handler(lambda c: c.data.split('_')[0] == 'mon')
async def process_callback_money(callback_query: types.CallbackQuery):
    money = random.randint(500, 1000)
    if callback_query.data.split('_')[1] == 'KZT':
        money *= 5.38
        res_money = f'{round(money,2)} Тг'
    elif callback_query.data.split('_')[1] == 'UAH':
        money *= 0.44
        res_money = f'{round(money,2)} Грн'
    elif callback_query.data.split('_')[1] == 'BYN':
        money *= 0.035
        res_money = f'{round(money,2)} Руб'
    elif callback_query.data.split('_')[1] == 'EUR':
        money *= 0.0109
        res_money = f'{round(money,2)} Евро'
    else:
        res_money = f'{round(money,2)} Руб'
    await callback_query.message.edit_reply_markup(None)
    await callback_query.message.answer(texts.money_success.format(res_money), reply_markup=kb.inline_get)

@dp.callback_query_handler(lambda c: c.data == 'get')
async def process_callback_get(callback_query: types.CallbackQuery):
    channels = get_channels()
    strin = ''
    for i, val in enumerate(channels, start=1):
        strin += f'{i}) <a href="{val[1]}">{val[0]}</a>\n'
    await callback_query.message.answer(text=texts.channels.format(strin), reply_markup=kb.inline_checked_get)

@dp.callback_query_handler(lambda c: c.data == 'check')
async def process_callback_check(callback_query: types.CallbackQuery):
    info = await bot.get_chat_member(chat_id=channel_id, user_id=callback_query.from_user.id)
    if info.status == 'left':
        await callback_query.answer(text=texts.subscribe, show_alert=True)
    else:
        await callback_query.message.answer(text=texts.final_success)
        