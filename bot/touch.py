import os
import sqlite3
from datetime import datetime


class Touch:
    def __init__(self, folder_path: str) -> None:
        self._ensure_folder_exists(folder_path)
        self.db_path: str = os.path.join(folder_path, "touch.db")
        self._initialize_db()

    def _ensure_folder_exists(self, folder_path: str) -> None:
        # Convert relative path to absolute path
        folder_path = os.path.abspath(folder_path)

        # Check if the folder exists before creating it
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    def _initialize_db(self) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Create a table if it does not exist
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS entities
                          (id INTEGER PRIMARY KEY, 
                           argument1 TEXT NOT NULL, 
                           argument2 TEXT NOT NULL, 
                           timestamp DATETIME NOT NULL,
                           UNIQUE(argument1, argument2))"""
        )
        conn.commit()
        conn.close()

    def touch_entity(self, argument1: str, argument2: str) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check if the entity already exists
        cursor.execute(
            "SELECT id FROM entities WHERE argument1 = ? AND argument2 = ?",
            (argument1, argument2),
        )
        if cursor.fetchone():
            conn.close()
            return True

        # Insert the entity since it does not exist
        now = datetime.now()
        cursor.execute(
            "INSERT INTO entities (argument1, argument2, timestamp) VALUES (?, ?, ?)",
            (argument1, argument2, now),
        )
        conn.commit()
        conn.close()
        return False
