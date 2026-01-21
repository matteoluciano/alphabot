import sqlite3

conn = sqlite3.connect("users.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

cur.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
    ("admin", "password"))

conn.commit()
conn.close()
