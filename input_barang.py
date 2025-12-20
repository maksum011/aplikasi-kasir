import sqlite3

conn = sqlite3.connect("toko.db")
cursor = conn.cursor()

data_barang = [
    ("8999999059347", "sabun Lifebuoy batang", 5000, 20),
    ("8992727000550", "sabun biore cair 250ml", 18000, 30),
    ("8999999603014", "sunlight cuci piring", 9000, 20),
    ("8999999600723", "Pepsodent", 6000, 15),
    ("8999999052973", "Pond's cuci muka", 17000, 15),
]

cursor.executemany(
    "INSERT OR REPLACE INTO barang VALUES (?, ?, ?, ?)",
    data_barang
)

conn.commit()
conn.close()

print("Data barang berhasil dimasukkan.")
