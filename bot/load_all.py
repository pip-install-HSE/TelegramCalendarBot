import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN




logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()
storage = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)