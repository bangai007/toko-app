import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Aplikasi Kasir & Stok", layout="wide")

# Dummy user data
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "karyawan": {"password": "123", "role": "karyawan"}
}

# Inisialisasi session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.penjualan_data = pd.DataFrame(columns=["Tanggal", "Nama Barang", "Jumlah", "Total"])
    st.session_state.stok_data = pd.DataFrame(columns=["Nama Barang", "Stok"])

# Fungsi logout
def logout():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()

# Halaman login
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

# Setelah login
st.sidebar.write(f"Logged in sebagai: {st.session_state.username} ({st.session_state.role})")
if st.sidebar.button("Logout"):
    logout()

# Menu sidebar berdasarkan role
if st.session_state.role == "admin":
    menu = st.sidebar.selectbox("Menu", ["Input Penjualan", "Stok Barang", "Riwayat Penjualan"])
else:
    menu = st.sidebar.selectbox("Menu", ["Input Penjualan"])

# Fungsi tambah stok barang (admin)
def tambah_stok(nama_barang, jumlah):
    stok_df = st.session_state.stok_data
    if nama_barang in stok_df["Nama Barang"].values:
        idx = stok_df.index[stok_df["Nama Barang"] == nama_barang][0]
        stok_df.at[idx, "Stok"] += jumlah
    else:
        new_row = {"Nama Barang": nama_barang, "Stok": jumlah}
        st.session_state.stok_data = pd.concat([stok_df, pd.DataFrame([new_row])], ignore_index=True)

# Fungsi kurangi stok (penjualan)
def kurangi_stok(nama_barang, jumlah):
    stok_df = st.session_state.stok_data
    if nama_barang in stok_df["Nama Barang"].values:
        idx = stok_df.index[stok_df["Nama Barang"] == nama_barang][0]
        if stok_df.at[idx, "Stok"] >= jumlah:
            stok_df.at[idx, "Stok"] -= jumlah
            return True
        else:
            return False
    else:
        return False

# Menu: Input Penjualan
if menu == "Input Penjualan":
    st.title("Input Penjualan")
    with st.form("form_penjualan"):
        tanggal = st.date_input("Tanggal", datetime.today())
        nama_barang = st.text_input("Nama Barang")
        jumlah = st.number_input("Jumlah", min_value=1, step=1)
        total = st.number_input("Total Harga (Rp)", min_value=0, step=100)
        submit = st.form_submit_button("Simpan Penjualan")

    if submit:
        if not nama_barang:
            st.error("Nama barang wajib diisi!")
        else:
            stok_ok = kurangi_stok(nama_barang, jumlah)
            if not stok_ok:
                st.error(f"Stok barang '{nama_barang}' tidak cukup atau belum ada.")
            else:
                new_penjualan = {
                    "Tanggal": tanggal.strftime("%Y-%m-%d"),
                    "Nama Barang": nama_barang,
                    "Jumlah": jumlah,
                    "Total": total
                }
                st.session_state.penjualan_data = pd.concat(
                    [st.session_state.penjualan_data, pd.DataFrame([new_penjualan])],
                    ignore_index=True
                )
                st.success(f"Penjualan {jumlah} {nama_barang} berhasil disimpan.")
    st.subheader("Data Penjualan Hari Ini")
    st.dataframe(st.session_state.penjualan_data)

# Menu: Stok Barang (admin)
elif menu == "Stok Barang":
    st.title("Manajemen Stok Barang")
    with st.form("form_stok"):
        nama_barang = st.text_input("Nama Barang Baru")
        jumlah = st.number_input("Jumlah Masuk", min_value=1, step=1)
        simpan = st.form_submit_button("Tambah Stok")

    if simpan:
        if not nama_barang:
            st.error("Nama barang wajib diisi!")
        else:
            tambah_stok(nama_barang, jumlah)
            st.success(f"Stok barang '{nama_barang}' berhasil ditambah sebanyak {jumlah}.")

    st.subheader("Daftar Stok Barang")
    st.dataframe(st.session_state.stok_data)

# Menu: Riwayat Penjualan (admin)
elif menu == "Riwayat Penjualan":
    st.title("Riwayat Penjualan")
    st.dataframe(st.session_state.penjualan_data)
