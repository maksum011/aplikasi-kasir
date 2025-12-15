import sqlite3

conn = sqlite3.connect("toko.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM transaksi")
data = cursor.fetchall()

conn.close()

for row in data:
    print(row)
