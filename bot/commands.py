from aiogram import types
from database import add_user, get_keywords

async def start_command(message: types.Message):
    await add_user(message.from_user.id)
    await message.answer("Привет! Я помогу тебе находить вакансии. Настрой ключевые слова с помощью /keywords")

async def profile_command(message: types.Message):
    keywords = await get_keywords(message.from_user.id)
    await message.answer(f"🔑 Твои ключевые слова:\n{keywords or 'Пока не задано'}")
