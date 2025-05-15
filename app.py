import streamlit as st

st.set_page_config(page_title="Login Demo", layout="wide")

# Data user (dummy)
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "karyawan": {"password": "123", "role": "karyawan"}
}

# Inisialisasi session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

# Tampilkan form login kalau belum login
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

# Setelah login berhasil
st.write(f"Selamat datang, {st.session_state.username}!")
st.write(f"Role Anda: {st.session_state.role}")
# Menu sidebar sederhana
menu = st.sidebar.selectbox("Menu", ["Input Penjualan"])

if menu == "Input Penjualan":
    st.header("Input Penjualan")
    with st.form("form_penjualan"):
        tanggal = st.date_input("Tanggal")
        nama_barang = st.text_input("Nama Barang")
        jumlah = st.number_input("Jumlah", min_value=1, step=1)
        total = st.number_input("Total Harga (Rp)", min_value=0, step=100)
        submit = st.form_submit_button("Simpan Penjualan")

    if submit:
        st.success(f"Penjualan {jumlah} {nama_barang} pada {tanggal} berhasil disimpan.")

