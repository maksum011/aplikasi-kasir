import sqlite3

conn = sqlite3.connect("toko.db")
c = conn.cursor()

users = [
    ("admin", "admin123", "admin"),
    ("kasir", "kasir123", "kasir")
]

c.executemany(
    "INSERT OR REPLACE INTO users VALUES (?, ?, ?)",
    users
)

conn.commit()
conn.close()

print("User admin & kasir dibuat.")
