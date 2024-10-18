import aiosqlite

DATABASE = 'rules.db'

async def init_db():
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rule_name TEXT,
                rule_text TEXT,
                rule_ast TEXT
            )
        ''')
        await db.commit()
