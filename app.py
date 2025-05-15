import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Aplikasi Harga & Keuangan", layout="wide")

st.title("Aplikasi Daftar Harga & Keuangan Harian")

# Fungsi bantu parsing rupiah dari string dengan titik ribuan
def parse_rupiah(s):
    try:
        return int(s.replace(".", ""))
    except:
        return 0

# Fungsi format angka jadi string dengan titik ribuan
def format_rupiah(x):
    return f"{x:,}".replace(",", ".")

# Inisialisasi session state untuk data harga dan keuangan
if "harga_barang" not in st.session_state:
    st.session_state.harga_barang = pd.DataFrame(columns=["Nama Barang", "Harga (Rp)"])

if "keuangan" not in st.session_state:
    st.session_state.keuangan = pd.DataFrame(columns=["Tanggal", "Keterangan", "Masuk (Rp)", "Keluar (Rp)"])

# --- Bagian Daftar Harga Barang ---
st.header("Daftar Harga Barang")

with st.form("form_harga"):
    nama_barang = st.text_input("Nama Barang")
    harga_str = st.text_input("Harga (Rp)", placeholder="1.000.000")
    submit_harga = st.form_submit_button("Tambah / Update Harga")

if submit_harga:
    harga = parse_rupiah(harga_str)
    if not nama_barang:
        st.error("Nama barang wajib diisi.")
    elif harga <= 0:
        st.error("Harga harus lebih dari 0.")
    else:
        df = st.session_state.harga_barang
        if nama_barang in df["Nama Barang"].values:
            idx = df.index[df["Nama Barang"] == nama_barang][0]
            st.session_state.harga_barang.at[idx, "Harga (Rp)"] = harga
            st.success(f"Harga {nama_barang} diperbarui menjadi Rp {format_rupiah(harga)}")
        else:
            new_row = {"Nama Barang": nama_barang, "Harga (Rp)": harga}
            st.session_state.harga_barang = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"{nama_barang} ditambahkan dengan harga Rp {format_rupiah(harga)}")

# Tampilkan tabel harga dengan format titik ribuan
df_display = st.session_state.harga_barang.copy()
df_display["Harga (Rp)"] = df_display["Harga (Rp)"].apply(format_rupiah)
st.dataframe(df_display, use_container_width=True)

# --- Bagian Keuangan Harian ---
st.header("Catatan Keuangan Harian")

with st.form("form_keuangan"):
    tanggal = st.date_input("Tanggal", date.today())
    keterangan = st.text_input("Keterangan")
    masuk_str = st.text_input("Pemasukan (Rp)", placeholder="1.000.000")
    keluar_str = st.text_input("Pengeluaran (Rp)", placeholder="500.000")
    submit_keuangan = st.form_submit_button("Catat Keuangan")

if submit_keuangan:
    masuk = parse_rupiah(masuk_str)
    keluar = parse_rupiah(keluar_str)
    if not keterangan:
        st.error("Keterangan wajib diisi.")
    elif masuk == 0 and keluar == 0:
        st.error("Pemasukan atau pengeluaran harus diisi lebih dari 0.")
    else:
        new_row = {
            "Tanggal": tanggal.strftime("%Y-%m-%d"),
            "Keterangan": keterangan,
            "Masuk (Rp)": masuk,
            "Keluar (Rp)": keluar
        }
        st.session_state.keuangan = pd.concat([st.session_state.keuangan, pd.DataFrame([new_row])], ignore_index=True)
        st.success("Catatan keuangan berhasil ditambahkan.")

# Tampilkan tabel keuangan dengan format titik ribuan
df_keu = st.session_state.keuangan.copy()
df_keu["Masuk (Rp)"] = df_keu["Masuk (Rp)"].apply(format_rupiah)
df_keu["Keluar (Rp)"] = df_keu["Keluar (Rp)"].apply(format_rupiah)
st.dataframe(df_keu, use_container_width=True)

# --- Ringkasan Keuangan ---
st.header("Ringkasan Keuangan")

total_masuk = st.session_state.keuangan["Masuk (Rp)"].sum()
total_keluar = st.session_state.keuangan["Keluar (Rp)"].sum()
saldo = total_masuk - total_keluar

st.markdown(f"""
- **Total Pemasukan:** Rp {format_rupiah(total_masuk)}  
- **Total Pengeluaran:** Rp {format_rupiah(total_keluar)}  
- **Saldo:** Rp {format_rupiah(saldo)}
""")
