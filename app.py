import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="Aplikasi Kasir & Stok", layout="wide")

# Data login manual (nanti bisa dikembangkan dari file/database)
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "karyawan": {"password": "123", "role": "karyawan"}
}

# Login Session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

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
    st.experimental_rerun()  # << Tambahan baris ini

        else:
            st.error("Username atau password salah.")
    st.stop()

import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="Aplikasi Kasir & Stok Toko", layout="wide")

# --- Load data dari session_state atau buat baru ---
if 'stok_data' not in st.session_state:
    st.session_state.stok_data = pd.DataFrame(columns=["Tanggal", "Nama Barang", "Masuk", "Keluar", "Sisa"])
if 'penjualan_data' not in st.session_state:
    st.session_state.penjualan_data = pd.DataFrame(columns=["Tanggal", "Nama Barang", "Jumlah", "Harga Satuan", "Total"])

# --- Fungsi ekspor ke Excel ---
def export_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

# --- Sidebar Menu ---
# Menu berdasarkan peran
role = st.session_state.role
if role == "admin":
    menu = st.sidebar.selectbox("Menu", ["Input Penjualan", "Stok Barang", "Riwayat Penjualan"])
else:
    menu = st.sidebar.selectbox("Menu", ["Input Penjualan"])

# --- Halaman Penjualan ---
if menu == "Input Penjualan":
    st.title("Input Penjualan Barang")
    with st.form("form_penjualan"):
        nama_barang = st.text_input("Nama Barang")
        jumlah = st.number_input("Jumlah", min_value=1, step=1)
        harga = st.number_input("Harga Satuan", min_value=0, step=100)
        submit = st.form_submit_button("Simpan Penjualan")

    if submit and nama_barang and jumlah:
        total = jumlah * harga
        tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Simpan penjualan
        new_row = pd.DataFrame([[tanggal, nama_barang, jumlah, harga, total]],
                               columns=st.session_state.penjualan_data.columns)
        st.session_state.penjualan_data = pd.concat([st.session_state.penjualan_data, new_row], ignore_index=True)

        # Otomatis kurangi stok
        stok_df = st.session_state.stok_data
        barang_mask = stok_df["Nama Barang"].str.lower() == nama_barang.lower()

        if barang_mask.any():
            idx = stok_df[barang_mask].index[-1]
            stok_df.at[idx, "Keluar"] += jumlah
            stok_df.at[idx, "Sisa"] = stok_df.at[idx, "Masuk"] - stok_df.at[idx, "Keluar"]
            st.success(f"Stok untuk '{nama_barang}' dikurangi otomatis.")
        else:
            st.warning(f"Barang '{nama_barang}' belum ada di data stok!")

    st.subheader("Riwayat Penjualan Hari Ini")
    st.dataframe(st.session_state.penjualan_data)

    st.download_button("Download Penjualan Excel", export_excel(st.session_state.penjualan_data), file_name="penjualan.xlsx")

# --- Halaman Stok Barang ---
# --- Halaman Stok Barang ---
elif menu == "Stok Barang":
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

    st.download_button(
        "Download Stok Excel",
        export_excel(st.session_state.stok_data),
        file_name="stok_barang.xlsx"
    )

# --- Halaman Riwayat ---
elif menu == "Riwayat Penjualan":
    st.title("Riwayat Penjualan Lengkap")
    st.dataframe(st.session_state.penjualan_data)
    st.download_button("Download Semua Penjualan", export_excel(st.session_state.penjualan_data), file_name="riwayat_penjualan.xlsx")

