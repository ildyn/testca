import aiosqlite

DB_NAME = "users.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                keywords TEXT,
                is_subscribed INTEGER DEFAULT 0
            )
        """)
        await db.commit()

async def add_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id, keywords) VALUES (?, '')", (user_id,))
        await db.commit()

async def update_keywords(user_id, keywords):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET keywords=? WHERE user_id=?", (keywords, user_id))
        await db.commit()

async def get_keywords(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT keywords FROM users WHERE user_id=?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else ""
