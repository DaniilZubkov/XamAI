import asyncpg
import logging
from typing import Optional, Dict, Any


class Database:
    _instance = None
    _pool: Optional[asyncpg.Pool] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def create_pool(self, **config):
        if self._pool is None:
            self._pool = await asyncpg.create_pool(
                min_size=5,
                max_size=20,
                **config
            )
            logging.info("Database pool created")

    async def register_user(self, user_data: Dict[str, Any]) -> Optional[int]:
        if not self._pool:
            raise RuntimeError("Pool is not initialized")

        async with self._pool.acquire() as conn:
            try:
                logging.info(f"Attempting to register user: {user_data['telegram_user_id']}")
                
                user_id = await conn.fetchval(
                    """
                    INSERT INTO users (
                        telegram_user_id, username, first_name, last_name, 
                        language_code, is_bot, is_premium, signup_source
                    )
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                    RETURNING id
                    """,
                    user_data['telegram_user_id'],
                    user_data.get('username'),
                    user_data['first_name'],
                    user_data.get('last_name'),
                    user_data.get('language_code'),
                    user_data.get('is_bot', False),
                    user_data.get('is_premium', False),
                    user_data.get('signup_source', 'telegram')
                )
                logging.info(f"New user registered with ID: {user_id}")
                return user_id
                
            except asyncpg.UniqueViolationError:
                logging.info(f"User already exists, updating: {user_data['telegram_user_id']}")
                await conn.execute(
                    """
                    UPDATE users SET
                        username = $2,
                        first_name = $3,
                        last_name = $4,
                        language_code = $5,
                        is_premium = $6,
                        updated_at = NOW(),
                        last_activity = NOW()
                    WHERE telegram_user_id = $1
                    """,
                    user_data['telegram_user_id'],
                    user_data.get('username'),
                    user_data['first_name'],
                    user_data.get('last_name'),
                    user_data.get('language_code'),
                    user_data.get('is_premium', False)
                )
                
                user_id = await conn.fetchval(
                    "SELECT id FROM users WHERE telegram_user_id = $1",
                    user_data['telegram_user_id']
                )
                logging.info(f"User data updated, ID: {user_id}")
                return user_id
                
            except Exception as e:
                logging.error(f"Error registering user {user_data['telegram_user_id']}: {e}", exc_info=True)
                return None

    async def get_user(self, telegram_user_id: int) -> Optional[Dict[str, Any]]:
        """Получает данные пользователя по telegram_user_id"""
        if not self._pool:
            raise RuntimeError("Pool is not initialized")

        async with self._pool.acquire() as conn:
            try:
                row = await conn.fetchrow(
                    "SELECT * FROM users WHERE telegram_user_id = $1",
                    telegram_user_id
                )
                return dict(row) if row else None
            except Exception as e:
                logging.error(f"Error getting user: {e}")
                return None

    async def update_last_activity(self, telegram_user_id: int):
        """Обновляет время последней активности пользователя"""
        if not self._pool:
            raise RuntimeError("Pool is not initialized")

        async with self._pool.acquire() as conn:
            try:
                await conn.execute(
                    "UPDATE users SET last_activity = NOW() WHERE telegram_user_id = $1",
                    telegram_user_id
                )
            except Exception as e:
                logging.error(f"Error updating last activity: {e}")

    async def get_user_count(self) -> int:
        """Возвращает общее количество пользователей"""
        if not self._pool:
            raise RuntimeError("Pool is not initialized")

        async with self._pool.acquire() as conn:
            try:
                count = await conn.fetchval("SELECT COUNT(*) FROM users")
                return count or 0
            except Exception as e:
                logging.error(f"Error getting user count: {e}")
                return 0

    async def close(self):
        if self._pool:
            await self._pool.close()
            self._pool = None
            logging.info("Database pool closed")
