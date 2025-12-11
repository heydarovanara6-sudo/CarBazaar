
import sqlite3
import os

DB_PATH = "users.db"

def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        print("Attempting to add 'views' column to 'car' table...")
        cursor.execute("ALTER TABLE car ADD COLUMN views INTEGER DEFAULT 0")
        conn.commit()
        print("Success: 'views' column added.")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e):
             print("Column 'views' already exists.")
        else:
            print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
