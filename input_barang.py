import sqlite3

# koneksi database
conn = sqlite3.connect("toko.db")
cursor = conn.cursor()

# HAPUS SEMUA DATA BARANG LAMA
cursor.execute("DELETE FROM barang")

# DATA BARANG BARU
data_barang = [
    ("8999999059347", "Sabun Lifebuoy Batang", 5000, 20),
    ("8992727000550", "Sabun Biore Cair 250ml", 18000, 30),
    ("8999999603014", "Sunlight Cuci Piring", 9000, 20),
    ("8999999600723", "Pepsodent", 6000, 15),
    ("8999999052973", "Pond's Cuci Muka", 17000, 15),
]

# MASUKKAN DATA BARANG
cursor.executemany(
    """
    INSERT INTO barang (barcode, nama, harga, stok)
    VALUES (?, ?, ?, ?)
    """,
    data_barang
)

conn.commit()
conn.close()

print("✅ Data barang lama dihapus & data baru berhasil dimasukkan.")
