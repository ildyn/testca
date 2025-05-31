from aiogram import types
from parser.telegram_parser import search_jobs_for_user
from database import update_keywords

async def set_keywords(message: types.Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.reply("Напиши ключевые слова через пробел, например:\n`/keywords python тестировщик`")
        return
    keywords = parts[1]
    await update_keywords(message.from_user.id, keywords)
    await message.reply("Ключевые слова обновлены!")

async def find_jobs(message: types.Message):
    await message.reply("🔍 Ищу вакансии по твоим ключевым словам...")
    await search_jobs_for_user(message.from_user.id, message.bot)

def register_handlers(dp):
    dp.register_message_handler(set_keywords, commands=['keywords'])
    dp.register_message_handler(find_jobs, commands=['find'])
