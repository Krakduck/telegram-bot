import sqlite3
import logging
# ========== НАСТРОЙКА ЛОГИРОВАНИЯ ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class UserDatabase:
    def __init__(self):
        # Определяем путь к БД
        self.db_path = '/data/bot_users.db'
        self.create_table()

    def create_table(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users ( 
                              telegram_id INTEGER PRIMARY KEY,
                              is_admin BOOLEAN NOT NULL,
                              credits INTEGER NOT NULL,
                              username TEXT NOT NULL,
                              password TEXT NOT NULL,
                              allowMEME BOOLEAN NOT NULL,
                              count_messages INTEGER NOT NULL,
                              rating INTEGER NOT NULL,
                              klichka TEXT NOT NULL)''')
        connection.commit()
        connection.close()

    def add_user(self, telegram_id, is_admin, credits, username, password, allowMEME,count_messages, rating,klichka):
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute(
                'INSERT INTO users (telegram_id, is_admin,credits, username, password, allowMEME, count_messages, rating, klichka) VALUES (?, ?, ?, ?, ?, ?, ?,?,?)',
                (telegram_id, is_admin, credits, username, password, allowMEME,count_messages, rating, klichka)
            )
            connection.commit()
            connection.close()
            return True
        except Exception as e:
            logger.info(f"Ошибка добавления: {e}")
            return False

    def get_user(self, telegram_id):
        try:
            connection = sqlite3.connect(self.db_path)

            cursor = connection.cursor()
            cursor.execute(
                'SELECT * FROM users WHERE telegram_id = ?',
                (telegram_id,)
            )
            result = cursor.fetchone()
            connection.close()

            if result:
                logger.info(f"RESULT ИЗ БАЗЫ: {result}")
                # В result порядок такой же как в CREATE TABLE:
                # (telegram_id, username, password, klichka)
                return {
                    'telegram_id': result[0],
                    'is_admin': result[1],
                    'credits': result[2],
                    'username': result[3],
                    'password': result[4],
                    'allowMEME': result[5],
                    'count_messages': result[6],
                    'rating': result[7],
                    'klichka': result[8]
                }
            return None
        except Exception as e:
            logger.info(f"Ошибка поиска: {e}")
            return None

    def get_all_users_stat(self):
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Выбираем только нужные колонки для всех строк
            cursor.execute("SELECT username, count_messages, rating, telegram_id FROM users")
            data = cursor.fetchall()

            connection.close()
            return data  # Вернет список вида: [('@user1', 100, 100, 123456789), ('@user2', 500, 100, 987654321)]
        except Exception as e:
            logger.info(f"Ошибка при получении статистики: {e}")
            return []


    def update_user_param(self, telegram_id, column_name, new_value):
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

        # Используем f-строку для названия колонки,
        # но знаки вопроса для значения (защита от взлома)
            query = f"UPDATE users SET {column_name} = ? WHERE telegram_id = ?"

            cursor.execute(query, (new_value, telegram_id))

            connection.commit()
            connection.close()
            return True
        except Exception as e:
            logger.info(f"Ошибка при обновлении {column_name}: {e}")
            return False