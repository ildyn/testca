from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
from bot.commands import start_command, profile_command
from bot.handlers import register_handlers
from database import init_db
import asyncio
import aiosqlite
from parser.telegram_parser import run_parser

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await start_command(message)

@dp.message_handler(commands=['profile'])
async def profile(message: types.Message):
    await profile_command(message)

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer("""
📌 Команды бота:
/start — начать работу
/profile — посмотреть ключевые слова
/keywords [слова] — задать ключевые слова
/find — найти вакансии по ключевым словам
""")
async def get_all_user_ids():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT user_id FROM users") as cursor:
            rows = await cursor.fetchall()
            return [r[0] for r in rows]

async def run_parser(bot, user_ids):
    from parser.telegram_parser import search_jobs_for_user
    for user_id in user_ids:
        await search_jobs_for_user(user_id, bot)

async def periodic_parsing():
    while False:
        user_ids = await get_all_user_ids()
        await run_parser(bot, user_ids)
        await asyncio.sleep(3600)

async def on_startup(dp):
    await init_db()
    print("Бот запущен.")

register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
