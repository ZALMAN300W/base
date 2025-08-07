from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from decouple import config


admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]

BOT_TOKEN = config("BOT_TOKEN")
HOST = config("HOST")
PORT = int(config("PORT"))
WEBHOOK_PATH = f'/{BOT_TOKEN}'
BASE_URL = config("BASE_URL")
CHANNEL_ID = config ("CHANNEL_ID")

bot = Bot(token=BOT_TOKEN, default= DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()