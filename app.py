import streamlit as st
import pandas as pd
import datetime
from io import BytesIO

st.set_page_config(page_title="Manajemen Toko", layout="wide")
st.title("📦 Aplikasi Manajemen Toko Sederhana")

if "keuangan" not in st.session_state:
    st.session_state.keuangan = []
if "stok" not in st.session_state:
    st.session_state.stok = []
if "karyawan" not in st.session_state:
    st.session_state.karyawan = []

menu = st.sidebar.radio("Menu", ["Keuangan", "Stok Barang", "Karyawan", "Laporan"])

# Fungsi ekspor ke Excel
def download_excel(data, filename):
    output = BytesIO()
    df = pd.DataFrame(data)
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
    st.download_button("📥 Download ke Excel", output.getvalue(), file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# KEUANGAN
if menu == "Keuangan":
    st.header("💰 Catatan Keuangan Harian")
    with st.form("form_keuangan"):
        tanggal = st.date_input("Tanggal", datetime.date.today())
        uraian = st.text_input("Uraian")
        pemasukan = st.number_input("Pemasukan (Rp)", min_value=0, step=1000)
        pengeluaran = st.number_input("Pengeluaran (Rp)", min_value=0, step=1000)
        keterangan = st.text_input("Keterangan")
        submitted = st.form_submit_button("Simpan")
        if submitted:
            st.session_state.keuangan.append({
                "Tanggal": tanggal,
                "Uraian": uraian,
                "Pemasukan (Rp)": pemasukan,
                "Pengeluaran (Rp)": pengeluaran,
                "Keterangan": keterangan
            })
            st.success("Data keuangan disimpan!")

    st.subheader("Data Keuangan")
    df_keuangan = pd.DataFrame(st.session_state.keuangan)
    st.dataframe(df_keuangan)
    if df_keuangan.shape[0] > 0:
        download_excel(st.session_state.keuangan, "keuangan.xlsx")

# STOK
elif menu == "Stok Barang":
    st.header("📦 Catatan Stok Barang")
    with st.form("form_stok"):
        tanggal = st.date_input("Tanggal", datetime.date.today())
        nama_barang = st.text_input("Nama Barang")
        stok_awal = st.number_input("Stok Awal", min_value=0)
        masuk = st.number_input("Barang Masuk", min_value=0)
        keluar = st.number_input("Barang Keluar (Terjual)", min_value=0)
        sisa = stok_awal + masuk - keluar
        keterangan = st.text_input("Keterangan")
        submitted = st.form_submit_button("Simpan")
        if submitted:
            st.session_state.stok.append({
                "Tanggal": tanggal,
                "Nama Barang": nama_barang,
                "Stok Awal": stok_awal,
                "Masuk": masuk,
                "Keluar": keluar,
                "Sisa": sisa,
                "Keterangan": keterangan
            })
            st.success("Data stok disimpan!")

    st.subheader("Data Stok Barang")
    df_stok = pd.DataFrame(st.session_state.stok)
    st.dataframe(df_stok)
    if df_stok.shape[0] > 0:
        download_excel(st.session_state.stok, "stok_barang.xlsx")

# KARYAWAN
elif menu == "Karyawan":
    st.header("👨‍💼 Catatan Karyawan")
    with st.form("form_karyawan"):
        tanggal = st.date_input("Tanggal", datetime.date.today())
        nama_karyawan = st.text_input("Nama Karyawan")
        jam_kerja = st.text_input("Jam Kerja")
        tugas = st.text_input("Catatan Tugas")
        evaluasi = st.text_input("Evaluasi Singkat")
        tindak_lanjut = st.text_input("Tindak Lanjut")
        submitted = st.form_submit_button("Simpan")
        if submitted:
            st.session_state.karyawan.append({
                "Tanggal": tanggal,
                "Nama Karyawan": nama_karyawan,
                "Jam Kerja": jam_kerja,
                "Catatan Tugas": tugas,
                "Evaluasi": evaluasi,
                "Tindak Lanjut": tindak_lanjut
            })
            st.success("Data karyawan disimpan!")

    st.subheader("Data Karyawan")
    df_karyawan = pd.DataFrame(st.session_state.karyawan)
    st.dataframe(df_karyawan)
    if df_karyawan.shape[0] > 0:
        download_excel(st.session_state.karyawan, "karyawan.xlsx")

# LAPORAN
elif menu == "Laporan":
    st.header("📊 Laporan Ringkas")
    if st.session_state.keuangan:
        df = pd.DataFrame(st.session_state.keuangan)
        total_masuk = df["Pemasukan (Rp)"].sum()
        total_keluar = df["Pengeluaran (Rp)"].sum()
        st.metric("Total Pemasukan", f"Rp {total_masuk:,.0f}")
        st.metric("Total Pengeluaran", f"Rp {total_keluar:,.0f}")
        st.metric("Laba / Rugi", f"Rp {total_masuk - total_keluar:,.0f}")
    else:
        st.info("Belum ada data keuangan.")
