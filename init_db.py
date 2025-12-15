import sqlite3

conn = sqlite3.connect("toko.db")
c = conn.cursor()

# tabel barang
c.execute("""
CREATE TABLE IF NOT EXISTS barang (
    barcode TEXT PRIMARY KEY,
    nama TEXT,
    harga INTEGER,
    stok INTEGER
)
""")

# tabel transaksi
c.execute("""
CREATE TABLE IF NOT EXISTS transaksi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tanggal TEXT,
    total INTEGER
)
""")

# tabel detail transaksi
c.execute("""
CREATE TABLE IF NOT EXISTS detail_transaksi (
    transaksi_id INTEGER,
    barcode TEXT,
    jumlah INTEGER,
    subtotal INTEGER
)
""")

# =====================
# TAMBAHAN STEP 1 (INI)
# =====================
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    role TEXT
)
""")

conn.commit()
conn.close()

print("Database + tabel users siap.")
