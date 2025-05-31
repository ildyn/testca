from telethon import TelegramClient
from config import API_ID, API_HASH
from database import get_keywords
import asyncio

SESSION_NAME = "parser_session"
GROUPS = [
    'https://t.me/jobforjunior',
    'https://t.me/remotejob_ru',
]

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def search_jobs_for_user(user_id, bot):
    keywords = await get_keywords(user_id)
    if not keywords:
        return

    key_list = [k.lower() for k in keywords.split()]
    found = []

    await client.start()
    for group in GROUPS:
        try:
            async for message in client.iter_messages(group, limit=50):
                if message.text:
                    text = message.text.lower()
                    if any(k in text for k in key_list):
                        found.append(message.text[:1000])
        except Exception as e:
            print(f"Ошибка парсинга {group}: {e}")

    if found:
        await bot.send_message(user_id, f"🔎 Найдено {len(found)} вакансий:")
        for f in found[:5]:
            await bot.send_message(user_id, f)
    else:
        await bot.send_message(user_id, "Новых вакансий не найдено.")
