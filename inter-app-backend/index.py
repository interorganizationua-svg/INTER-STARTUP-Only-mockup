import asyncio
from aiogram import Bot, Dispatcher, html, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.types import FSInputFile

import random
from datetime import datetime, timedelta, time

from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.types import InlineKeyboardButton, KeyboardButton, WebAppInfo

from aiohttp import web


from setting import *

import time

from aiogram import F
import json


Index = Router()

current_datetimer = datetime.now()



@Index.message(CommandStart())
async def start(message: Message, state: FSMContext):
    chat_id = message.chat.id



    await state.clear()

    user_id[chat_id] = {'chat_id': chat_id}

    print(user_id)
    
    id_sticker = 'CAACAgUAAxkBAAIHZGdvht5LhSzUwjKpxFH58agzjLJGAAKGDQACLObRVNWwB0jZdX_oNgQ'
    await message.answer_sticker(id_sticker)

    tg_name = message.chat.username
    text_start = (f'Привет {tg_name}!, <b>Покупай звезды быстро</b>\n\nМы не требуем верификацию и быстро присылаем.')
    
    inter_button = [[InlineKeyboardButton(text='Buy Stars', web_app=WebAppInfo(url=f'https://URl_link_site/?chat_id={chat_id}')), InlineKeyboardButton(text='Community', url='url_channel')]]
    all_button = InlineKeyboardMarkup(inline_keyboard=inter_button)

    await message.answer(text_start, reply_markup=all_button, parse_mode='HTML')
