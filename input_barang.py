import sqlite3

conn = sqlite3.connect("toko.db")
cursor = conn.cursor()

data_barang = [
    ("1234567890123", "Indomie Goreng", 3500, 50),
    ("9876543210987", "Teh Botol", 4000, 30),
    ("1112223334445", "Susu UHT", 6000, 20)
]

cursor.executemany(
    "INSERT OR REPLACE INTO barang VALUES (?, ?, ?, ?)",
    data_barang
)

conn.commit()
conn.close()

print("Data barang berhasil dimasukkan.")
