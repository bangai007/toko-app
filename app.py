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
if "penjualan" not in st.session_state:
    st.session_state.penjualan = []

menu = st.sidebar.radio("Menu", ["Penjualan", "Keuangan", "Stok Barang", "Karyawan", "Laporan"])

def download_excel(data, filename):
    output = BytesIO()
    df = pd.DataFrame(data)
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
    st.download_button("📥 Download ke Excel", output.getvalue(), file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# ✅ PENJUALAN
if menu == "Penjualan":
    st.header("🧾 Cetak Nota Penjualan")
    with st.form("form_penjualan"):
        tanggal = st.date_input("Tanggal", datetime.date.today())
        nama_pembeli = st.text_input("Nama Pembeli")
        nama_barang = st.text_input("Nama Barang")
        harga = st.number_input("Harga Satuan", min_value=0, step=1000)
        jumlah = st.number_input("Jumlah", min_value=1)
        total = harga * jumlah
        keterangan = st.text_input("Keterangan tambahan (opsional)")
        submitted = st.form_submit_button("Simpan Transaksi")
        if submitted:
            st.session_state.penjualan.append({
                "Tanggal": tanggal,
                "Pembeli": nama_pembeli,
                "Barang": nama_barang,
                "Harga Satuan": harga,
                "Jumlah": jumlah,
                "Total": total,
                "Keterangan": keterangan
            })
            st.success("Transaksi disimpan!")

    if st.session_state.penjualan:
        st.subheader("Riwayat Penjualan Hari Ini")
        df_penjualan = pd.DataFrame(st.session_state.penjualan)
        st.dataframe(df_penjualan)
        download_excel(st.session_state.penjualan, "penjualan.xlsx")

        st.subheader("🖨️ Cetak Nota")
        for i, trx in enumerate(reversed(st.session_state.penjualan[-5:])):
            nota = f"""
=========================
      NOTA PENJUALAN
=========================
Tanggal    : {trx['Tanggal']}
Pembeli    : {trx['Pembeli']}
Barang     : {trx['Barang']}
Harga      : Rp {trx['Harga Satuan']:,.0f}
Jumlah     : {trx['Jumlah']}
-------------------------
Total Bayar: Rp {trx['Total']:,.0f}
{f"Keterangan : " + trx['Keterangan'] if trx['Keterangan'] else ""}
=========================
Terima kasih 🙏
"""
            st.code(nota, language="text")

# 💰 KEUANGAN
elif menu == "Keuangan":
    st.header("💰 Catatan Keuangan Harian")
    with st.form("form_keuangan"):
        tanggal = st.date_input("Tanggal", datetime.date.today())
        uraian = st.text_input("Uraian")
        pemasukan = st.number_input("Pemasukan (Rp)", min_value=0, step=1000)
        pengeluaran = st.number_input("Pengeluaran (Rp)", min_value=0, step=1000)
        keterangan = st.text_input("Keterangan")
        submitted = st.form_submit_button("Simpan")
        if submitted:
            st.session_state.ke_
