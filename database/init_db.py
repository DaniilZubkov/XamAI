import asyncio
import asyncpg
import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from config.settings import DB_CONFIG




logger = logging.getLogger(__name__)

async def init_db():
    conn = None
    try:
        conn = await asyncpg.connect(
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
            port=int(DB_CONFIG["port"]),
            database="postgres"
        )
        
        await conn.execute(f"""
            CREATE DATABASE {DB_CONFIG['database']}
            ENCODING 'UTF8'
            LC_COLLATE 'ru_RU.UTF-8'
            LC_CTYPE 'ru_RU.UTF-8'
        """)
        logger.info(f"Database {DB_CONFIG['database']} created")
    except asyncpg.DuplicateDatabaseError:
        logger.info(f"Database {DB_CONFIG['database']} already exists")
    except Exception as e:
        logger.error(f"Error creating database: {e}")
    finally:
        if conn:
            await conn.close()

    try:
        conn = await asyncpg.connect(
            database=DB_CONFIG['database'],
            **{k: v for k, v in DB_CONFIG.items() if k != 'database'}
        )
        
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS "users" (
                id SERIAL PRIMARY KEY,
                telegram_user_id BIGINT UNIQUE NOT NULL,
                username VARCHAR(255), -- Может быть NULL
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255),
                language_code VARCHAR(10),
                is_bot BOOLEAN DEFAULT FALSE,
                is_premium BOOLEAN DEFAULT FALSE,
                signup_source VARCHAR(60) DEFAULT 'telegram',
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW(),
                last_activity TIMESTAMP DEFAULT NOW()
            );
        """)
        
        # Создание индексов для оптимизации поиска
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_telegram_id 
            ON users(telegram_user_id)
        """)
        
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_username 
            ON users(username) WHERE username IS NOT NULL
        """)
        
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_created_at 
            ON users(created_at)
        """)
        
        logger.info("Tables and indexes created successfully")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
    finally:
        if conn:
            await conn.close()

if __name__ == "__main__":
    asyncio.run(init_db())
