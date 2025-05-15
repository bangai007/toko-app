import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Aplikasi Harga & Keuangan", layout="wide")

st.title("Aplikasi Daftar Harga & Keuangan Harian")

# Inisialisasi session state untuk data harga dan keuangan
if "harga_barang" not in st.session_state:
    st.session_state.harga_barang = pd.DataFrame(columns=["Nama Barang", "Harga (Rp)"])

if "keuangan" not in st.session_state:
    st.session_state.keuangan = pd.DataFrame(columns=["Tanggal", "Keterangan", "Masuk (Rp)", "Keluar (Rp)"])

# --- Bagian Daftar Harga Barang ---
st.header("Daftar Harga Barang")

with st.form("form_harga"):
    nama_barang = st.text_input("Nama Barang")
    harga = st.number_input("Harga (Rp)", min_value=0, step=100)
    submit_harga = st.form_submit_button("Tambah / Update Harga")

if submit_harga:
    if not nama_barang:
        st.error("Nama barang wajib diisi.")
    else:
        df = st.session_state.harga_barang
        if nama_barang in df["Nama Barang"].values:
            # Update harga
            idx = df.index[df["Nama Barang"] == nama_barang][0]
            st.session_state.harga_barang.at[idx, "Harga (Rp)"] = harga
            st.success(f"Harga {nama_barang} diperbarui menjadi Rp {harga:,}")
        else:
            # Tambah data baru
            new_row = {"Nama Barang": nama_barang, "Harga (Rp)": harga}
            st.session_state.harga_barang = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"{nama_barang} ditambahkan dengan harga Rp {harga:,}")

st.dataframe(st.session_state.harga_barang)

# --- Bagian Keuangan Harian ---
st.header("Catatan Keuangan Harian")

with st.form("form_keuangan"):
    tanggal = st.date_input("Tanggal", date.today())
    keterangan = st.text_input("Keterangan")
    masuk = st.number_input("Pemasukan (Rp)", min_value=0, step=100)
    keluar = st.number_input("Pengeluaran (Rp)", min_value=0, step=100)
    submit_keuangan = st.form_submit_button("Catat Keuangan")

if submit_keuangan:
    if not keterangan:
        st.error("Keterangan wajib diisi.")
    else:
        new_row = {
            "Tanggal": tanggal.strftime("%Y-%m-%d"),
            "Keterangan": keterangan,
            "Masuk (Rp)": masuk,
            "Keluar (Rp)": keluar
        }
        st.session_state.keuangan = pd.concat([st.session_state.keuangan, pd.DataFrame([new_row])], ignore_index=True)
        st.success("Catatan keuangan berhasil ditambahkan.")

st.dataframe(st.session_state.keuangan)

# --- Ringkasan Keuangan ---
st.header("Ringkasan Keuangan")

total_masuk = st.session_state.keuangan["Masuk (Rp)"].sum()
total_keluar = st.session_state.keuangan["Keluar (Rp)"].sum()
saldo = total_masuk - total_keluar

st.write(f"**Total Pemasukan:** Rp {total_masuk:,}")
st.write(f"**Total Pengeluaran:** Rp {total_keluar:,}")
st.write(f"**Saldo:** Rp {saldo:,}")
