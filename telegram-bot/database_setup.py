
import sqlite3
from pathlib import Path

from config import DB_PATH


def init_db(db_path: Path | None = None) -> Path:
    db_file = db_path or DB_PATH
    db_file.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_file))
    cursor = conn.cursor()

    # Create service_logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS service_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            technician_name TEXT NOT NULL,
            device_id TEXT NOT NULL,
            user_name TEXT NOT NULL,
            user_email TEXT,
            service_done TEXT NOT NULL,
            parts_used TEXT,
            status TEXT NOT NULL DEFAULT 'Pending Confirmation',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_chat_id INTEGER,
            technician_chat_id INTEGER,
            confirmation_message_id INTEGER,
            delivery_method TEXT DEFAULT 'telegram'
        )
    ''')

    existing_columns = {
        row[1] for row in cursor.execute("PRAGMA table_info(service_logs)")
    }

    if 'user_email' not in existing_columns:
        cursor.execute("ALTER TABLE service_logs ADD COLUMN user_email TEXT")
    if 'delivery_method' not in existing_columns:
        cursor.execute("ALTER TABLE service_logs ADD COLUMN delivery_method TEXT DEFAULT 'telegram'")

    # Create confirmations table for digital signatures
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS confirmations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_log_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            user_telegram_name TEXT,
            confirmed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (service_log_id) REFERENCES service_logs(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS app_settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')

    conn.commit()
    conn.close()
    return db_file


if __name__ == '__main__':
    db_file = init_db()
    print(f"SQLite database '{db_file}' initialized with service_logs, confirmations, and app_settings tables.")
