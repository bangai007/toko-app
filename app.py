import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="Aplikasi Kasir & Stok", layout="wide")

# Dummy data user
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "karyawan": {"password": "123", "role": "karyawan"}
}

# Setup session login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

# FORM LOGIN
if not st.session_state.logged_in:
    st.title("Login Toko")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = USERS.get(username)
        if user and user["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = user["role"]
            st.success(f"Selamat datang, {username}!")
            st.experimental_rerun()
        else:
            st.error("Username atau password salah.")
    st.stop()

# Setelah login sukses
role = st.session_state.role
if role == "admin":
    menu = st.sidebar.selectbox("Menu", ["Input Penjualan", "Stok Barang", "Riwayat Penjualan"])
else:
    menu = st.sidebar.selectbox("Menu", ["Input Penjualan"])

# Simpan data stok jika belum ada
if "stok_data" not in st.session_state:
    st.session_state.stok_data = pd.DataFrame(columns=["Tanggal", "Nama Barang", "Masuk", "Keluar", "Sisa"])
if "penjualan_data" not in st.session_state:
    st.session_state.penjualan_data = pd.DataFrame(columns=["Tanggal", "Nama Barang", "Jumlah", "Total"])

# Menu: Input Penjualan
if menu == "Input Penjualan":
    st.title("Input Penjualan")
    with st.form("form_penjualan"):
        tanggal = st.date_input("Tanggal", datetime.today())
        nama_barang = st.text_input("Nama Barang")
        jumlah = st.number_input("Jumlah", min_value=1, step=1)
        total = st.number_input("Total Harga (Rp)", min_value=0, step=100)
        simpan = st.form_submit_button("Simpan Penjualan")

    if simpan and nama_barang and jumlah:
        tanggal_str = tanggal.strftime("%Y-%m-%d")
        new_row = {
            "Tanggal": tanggal_str,
            "Nama Barang": nama_barang,
            "Jumlah": jumlah,
            "Total": total
        }
        st.session_state.penjualan_data = pd.concat(
            [st.session_state.penjualan_data, pd.DataFrame([new_row])],
            ignore_index=True
        )

        # Update stok otomatis
        stok_df = st.session_state.stok_data
        match = stok_df["Nama Barang"] == nama_barang
        if match.any():
            idx = stok_df[match].index[-1]  # ambil entri terakhir
            stok_df.at[idx, "Keluar"] += jumlah
            stok_df.at[idx, "Sisa"] -= jumlah
        st.success("Data penjualan disimpan.")

    st.subheader("Data Penjualan")
    st.dataframe(st.session_state.penjualan_data)

# Menu: Stok Barang
elif menu == "Stok Barang" and role == "admin":
    st.title("Manajemen Stok Barang")

    with st.form("form_stok"):
        tanggal = st.date_input("Tanggal Input", datetime.today())
        nama_barang = st.text_input("Nama Barang Baru")
        masuk = st.number_input("Jumlah Masuk", min_value=0, step=1)
        simpan = st.form_submit_button("Simpan")

    if simpan:
        if nama_barang and masuk > 0:
            tanggal_str = tanggal.strftime("%Y-%m-%d")
            new_row = {
                "Tanggal": tanggal_str,
                "Nama Barang": nama_barang,
                "Masuk": masuk,
                "Keluar": 0,
                "Sisa": masuk
            }
            st.session_state.stok_data = pd.concat(
                [st.session_state.stok_data, pd.DataFrame([new_row])],
                ignore_index=True
            )
            st.success(f"Stok barang '{nama_barang}' berhasil ditambahkan.")
        else:
            st.warning("Isi nama barang dan jumlah masuk lebih dari 0.")

    st.subheader("Daftar Stok Barang")
    st.dataframe(st.session_state.stok_data)

# Menu: Riwayat Penjualan
elif menu == "Riwayat Penjualan" and role == "admin":
    st.title("Riwayat Penjualan")
    st.dataframe(st.session_state.penjualan_data)
