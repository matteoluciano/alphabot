import sqlite3

# Database degli utenti
conn_users = sqlite3.connect("users.db")
cur_users = conn_users.cursor()

cur_users.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

cur_users.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
    ("admin", "password"))

conn_users.commit()
conn_users.close()

# Database dei comandi
conn_commands = sqlite3.connect("commands.db")
cur_commands = conn_commands.cursor()

cur_commands.execute("""
CREATE TABLE IF NOT EXISTS commands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    username TEXT NOT NULL,
    command TEXT NOT NULL,
    executed INTEGER DEFAULT 0,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

conn_commands.commit()
conn_commands.close()

print("Database inizializzati correttamente!")
