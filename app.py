import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# =====================
# KONFIGURASI APLIKASI
# =====================
st.set_page_config(page_title="Aplikasi Kasir", layout="centered")
st.title("🧾 Aplikasi Kasir Toko")

# =====================
# KONEKSI DATABASE
# =====================
def get_conn():
    return sqlite3.connect("toko.db", check_same_thread=False)

conn = get_conn()
cursor = conn.cursor()

# =====================
# SESSION STATE
# =====================
if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.user = None
    st.session_state.role = None

# =====================
# HALAMAN LOGIN
# =====================
def login_page():
    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        cursor.execute(
            "SELECT role FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cursor.fetchone()

        if user:
            st.session_state.login = True
            st.session_state.user = username
            st.session_state.role = user[0]
            st.success("Login berhasil")
            st.rerun()
        else:
            st.error("Username atau password salah")

# =====================
# BUNGKUS MENU UTAMA
# =====================
if not st.session_state.login:
    login_page()
    st.stop()

# =====================
# SIDEBAR MENU
# =====================
st.sidebar.success(
    f"Login sebagai {st.session_state.user} ({st.session_state.role})"
)

menu_list = ["Kasir"]
if st.session_state.role == "admin":
    menu_list += ["Cek Stok", "Laporan Harian"]

menu = st.sidebar.selectbox("Menu", menu_list)

if st.sidebar.button("Logout"):
    st.session_state.login = False
    st.session_state.user = None
    st.session_state.role = None
    st.rerun()

# =====================
# MENU KASIR
# =====================
if menu == "Kasir":
    st.subheader("Kasir")

    if "keranjang" not in st.session_state:
        st.session_state.keranjang = {}

    st.markdown("### Scan / Masukkan Barcode")
    st.info("Gunakan barcode scanner atau ketik manual")

    barcode = st.text_input("Barcode Barang")

    if barcode:
        cursor.execute(
            "SELECT nama, harga, stok FROM barang WHERE barcode=?",
            (barcode,)
        )
        data = cursor.fetchone()

        if data:
            nama, harga, stok = data

            st.write("Nama:", nama)
            st.write("Harga:", f"Rp {harga}")
            st.write("Stok:", stok)

            jumlah = st.number_input(
                "Jumlah",
                min_value=1,
                max_value=stok,
                step=1
            )

            if st.button("Tambah ke Keranjang"):
                if barcode in st.session_state.keranjang:
                    st.session_state.keranjang[barcode]["jumlah"] += jumlah
                else:
                    st.session_state.keranjang[barcode] = {
                        "nama": nama,
                        "harga": harga,
                        "jumlah": jumlah
                    }
                st.success("Barang ditambahkan ke keranjang")
        else:
            st.error("Barang tidak ditemukan")

    # =====================
    # KERANJANG
    # =====================
    st.subheader("Keranjang")

    total_bayar = 0
    hapus_barcode = None

    for barcode, item in st.session_state.keranjang.items():
        col1, col2, col3, col4 = st.columns([4, 2, 2, 1])

        with col1:
            st.write(item["nama"])

        with col2:
            qty_baru = st.number_input(
                "Qty",
                min_value=1,
                value=item["jumlah"],
                key=f"qty_{barcode}"
            )

        with col3:
            subtotal = qty_baru * item["harga"]
            st.write(f"Rp {subtotal}")

        with col4:
            if st.button("❌", key=f"hapus_{barcode}"):
                hapus_barcode = barcode

        item["jumlah"] = qty_baru
        total_bayar += subtotal

    if hapus_barcode:
        del st.session_state.keranjang[hapus_barcode]
        st.rerun()

    st.write("### Total Bayar:", f"Rp {total_bayar}")

    # =====================
    # BAYAR
    # =====================
    if st.button("Bayar"):
        if total_bayar == 0:
            st.warning("Keranjang masih kosong")
        else:
            tanggal = datetime.now().strftime("%Y-%m-%d")

            cursor.execute(
                "INSERT INTO transaksi (tanggal, total) VALUES (?, ?)",
                (tanggal, total_bayar)
            )
            transaksi_id = cursor.lastrowid

            for barcode, item in st.session_state.keranjang.items():
                subtotal = item["jumlah"] * item["harga"]

                cursor.execute(
                    "INSERT INTO detail_transaksi VALUES (?, ?, ?, ?)",
                    (transaksi_id, barcode, item["jumlah"], subtotal)
                )

                cursor.execute(
                    "UPDATE barang SET stok = stok - ? WHERE barcode = ?",
                    (item["jumlah"], barcode)
                )

            conn.commit()
            st.session_state.keranjang = {}
            st.success("Transaksi berhasil disimpan")

# =====================
# MENU CEK STOK
# =====================
elif menu == "Cek Stok":
    st.subheader("Stok Barang")
    cursor.execute("SELECT barcode, nama, harga, stok FROM barang")
    st.table(cursor.fetchall())

# =====================
# MENU LAPORAN
# =====================
elif menu == "Laporan Harian":
    st.subheader("Laporan Pemasukan Harian")

    query = """
        SELECT tanggal, SUM(total) AS total_pemasukan
        FROM transaksi
        GROUP BY tanggal
        ORDER BY tanggal DESC
    """

    df = pd.read_sql_query(query, conn)
    st.dataframe(df, use_container_width=True)

    if not df.empty:
        file_name = "laporan_penjualan.xlsx"
        df.to_excel(file_name, index=False)

        with open(file_name, "rb") as f:
            st.download_button(
                "📥 Download Laporan Excel",
                data=f,
                file_name=file_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.info("Belum ada data transaksi")
