import sqlite3

conn = sqlite3.connect("toko.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM barang")
data = cursor.fetchall()

conn.close()

print(data)
