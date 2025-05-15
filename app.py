import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Aplikasi Toko", layout="wide")

st.title("🛒 Aplikasi Toko Sederhana")

# Inisialisasi data
if "barang" not in st.session_state:
    st.session_state.barang = pd.DataFrame(columns=["Nama", "Stok (pcs)", "Harga per pcs"])

if "penjualan" not in st.session_state:
    st.session_state.penjualan = pd.DataFrame(columns=["Tanggal", "Barang", "Jumlah", "Satuan", "Total (Rp)"])

# Konversi satuan ke pcs
konversi_satuan = {
    "pcs": 1,
    "pak": 10,
    "lusin": 12,
    "renteng": 6,
    "dus": 40
}

def format_rupiah(x):
    return f"{x:,}".replace(",", ".")

def parse_rupiah(s):
    try:
        return int(s.replace(".", ""))
    except:
        return 0

st.header("📦 Tambah Barang")
with st.form("form_barang"):
    nama = st.text_input("Nama Barang", key="nama_barang")
    stok = st.number_input("Stok Awal (pcs)", min_value=0, step=1, key="stok_barang")
    harga_str = st.text_input("Harga per pcs (Rp)", key="harga_barang", placeholder="1.000")

    submit_barang = st.form_submit_button("Tambah / Update Barang")

if submit_barang:
    harga = parse_rupiah(harga_str)
    if not nama:
        st.error("Nama barang wajib diisi.")
    elif harga <= 0:
        st.error("Harga harus lebih dari 0.")
    else:
        df = st.session_state.barang
        if nama in df["Nama"].values:
            idx = df.index[df["Nama"] == nama][0]
            st.session_state.barang.at[idx, "Stok (pcs)"] += stok
            st.session_state.barang.at[idx, "Harga per pcs"] = harga
            st.success("Barang diperbarui.")
        else:
            new = pd.DataFrame([{"Nama": nama, "Stok (pcs)": stok, "Harga per pcs": harga}])
            st.session_state.barang = pd.concat([df, new], ignore_index=True)
            st.success("Barang ditambahkan.")

        # Bersihkan input
        st.session_state.nama_barang = ""
        st.session_state.stok_barang = 0
        st.session_state.harga_barang = ""
        st.experimental_rerun()

st.subheader("📋 Daftar Barang")
df_display = st.session_state.barang.copy()
df_display["Harga per pcs"] = df_display["Harga per pcs"].apply(format_rupiah)
st.dataframe(df_display, use_container_width=True)

# -----------------------------
st.header("🧾 Penjualan Barang")
with st.form("form_jual"):
    if st.session_state.barang.empty:
        st.warning("Belum ada barang. Tambahkan dulu.")
    else:
        barang_pilihan = st.selectbox("Pilih Barang", st.session_state.barang["Nama"].tolist(), key="jual_barang")
        satuan = st.selectbox("Satuan", list(konversi_satuan.keys()), key="jual_satuan")
        jumlah = st.number_input("Jumlah", min_value=1, step=1, key="jual_jumlah")
        tgl = st.date_input("Tanggal", date.today())
        submit_jual = st.form_submit_button("Simpan Penjualan")

if 'submit_jual' in locals() and submit_jual:
    df = st.session_state.barang
    idx = df.index[df["Nama"] == barang_pilihan][0]
    jumlah_pcs = jumlah * konversi_satuan[satuan]

    if df.at[idx, "Stok (pcs)"] < jumlah_pcs:
        st.error("Stok tidak cukup!")
    else:
        harga_pcs = df.at[idx, "Harga per pcs"]
        total = harga_pcs * jumlah_pcs

        # Kurangi stok
        st.session_state.barang.at[idx, "Stok (pcs)"] -= jumlah_pcs

        # Simpan transaksi
        new_row = {
            "Tanggal": tgl.strftime("%Y-%m-%d"),
            "Barang": barang_pilihan,
            "Jumlah": jumlah,
            "Satuan": satuan,
            "Total (Rp)": total
        }
        st.session_state.penjualan = pd.concat([st.session_state.penjualan, pd.DataFrame([new_row])], ignore_index=True)
        st.success(f"Berhasil menjual {jumlah} {satuan} {barang_pilihan} (Rp {format_rupiah(total)})")

        # Bersihkan input
        st.session_state.jual_barang = st.session_state.barang["Nama"].iloc[0]
        st.session_state.jual_satuan = "pcs"
        st.session_state.jual_jumlah = 1
        st.experimental_rerun()

# -----------------------------
st.subheader("🗒️ Riwayat Penjualan")
if st.session_state.penjualan.empty:
    st.info("Belum ada penjualan.")
else:
    dfjual = st.session_state.penjualan.copy()
    dfjual["Total (Rp)"] = dfjual["Total (Rp)"].apply(format_rupiah)
    st.dataframe(dfjual, use_container_width=True)

    total_semua = st.session_state.penjualan["Total (Rp)"].sum()
    st.markdown(f"### 💰 Total Penjualan: Rp {format_rupiah(total_semua)}")
