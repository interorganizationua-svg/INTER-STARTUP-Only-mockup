import asyncio
import ssl
import logging
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from setting import *
from aiogram import F
from aiogram.types import Message
import index
import uvicorn

from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
logging.basicConfig(filemode='a', level=logging.INFO)

def fake_answer_to_everything_ml_model(x: float):
    return x * 42


ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.delete_webhook()
    dp.include_router(index.Index)

    polling_task  = asyncio.create_task(dp.start_polling(bot))

    yield  # Переходимо до обробки запитів

    polling_task.cancel()
    try:
        await polling_task
    except asyncio.CancelledError:
        pass

    ml_models.clear()

#Ініціалізація FastAPI
app = FastAPI(lifespan=lifespan)

origins = [
    "*",
]

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Обробка стікера
@dp.message(F.sticker)
async def auto_id(message: Message):
    print(f"Sticker ID: {message.sticker.file_id}")


#Роутинг
@app.get("/")
async def root():
    return {"message": "Сервер працює"}

@app.get("/payment")
async def payment_get():
    return PlainTextResponse("Цей маршрут лише для POST-запитів.")

@app.post("/payment")
async def payment_post(request: Request):
    try:
        data = await request.json()
    except:
        return JSONResponse({'status': 'error', 'message': 'Invalid JSON'}, status_code=400)

    chat_id = data.get("chat_id")
    quantity = data.get("quantity", 1)
    username = data.get("username", "unknown")
    total = data.get("total", "не вказано")

    manager_id = 'None'

    if not chat_id:
        return JSONResponse({'status': 'error', 'message': 'chat_id missing'}, status_code=400)

    inter_button = [
        [InlineKeyboardButton(text='Отменить', callback_data='cancell_order'),
         InlineKeyboardButton(text='Подтвердить', callback_data='yes_order')]
    ]
    all_button = InlineKeyboardMarkup(inline_keyboard=inter_button)

    inter_buttons = [
        [InlineKeyboardButton(text='Отменить', callback_data='cancell_order_')]
        ]
    all_buttons = InlineKeyboardMarkup(inline_keyboard=inter_buttons)

    try:
        await bot.send_message(
            chat_id,
            f"Проверка платежа (10-45 мин):\n"
            f"Транзакция: #TX{chat_id}\n"
            f"Количество: {quantity} ⭐\n"
            f"Пользователь: @{username}\n"
            f"Сумма: {total}", reply_markup=all_buttons
        )

        await bot.send_message(
            manager_id,
            f"Транзакция: #TX{chat_id}\n"
            f"Количество: {quantity} ⭐\n"
            f"Пользователь: @{username}\n"
            f"Сумма: {total}",
            reply_markup=all_button
        )

        return {"status": "ok"}

    except Exception as e:
        logging.error(f'ERROR {e}')
        return JSONResponse({'status': 'error', 'message': 'server error'}, status_code=500)

@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)
    

@app.get("/predict")
async def predict(x: float):
    model = ml_models.get("answer_to_everything")
    
    if not model:
        return JSONResponse({"error": "Model not loaded"}, status_code=500)

    result = ml_models["answer_to_everything"](x)
    return {"result": result}

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host="0.0.0.0", reload=True)