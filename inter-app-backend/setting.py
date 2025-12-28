from aiogram.fsm.storage.memory import MemoryStorage

from aiogram import Bot, Dispatcher, html, Router, F, types

TOKEN = ('<YOUR_TOKEN>')
ADMIN_ID = None

WEBHOOK_PATH = f"/bot/{TOKEN}"
RENDER_WEB_SERVICE_NAME = "<YOUR_RENDER_WEB_SERVICE_NAME>"
WEBHOOK_URL = "https://" + RENDER_WEB_SERVICE_NAME + ".onrender.com" + WEBHOOK_PATH

bot = Bot(token=TOKEN)
storage = MemoryStorage()

dp = Dispatcher(storage=storage)

user_commnets = {}

starts_coun_global = {}
ton_counts = {}

user_data = {}

last_activity = {}

user_id = {}


timer_adders = {}

cancell_st = {}
confirm_st = {}

user_balance = {}