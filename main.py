# main.py
import sys
import os
import sqlite3
from gui import ConverterApp

DB_PATH = "history.db"

def init_db():
    """Initialize the SQLite database for conversion history."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            conversion_type TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()  # Create the database if it doesn't exist.
    
    # Initialize and run the PyQt6 application.
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    converter_app = ConverterApp()
    converter_app.show()
    sys.exit(app.exec())

