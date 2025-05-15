import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Aplikasi Toko", layout="wide")

st.title("🛒 Aplikasi Toko & Keuangan Harian")

# Inisialisasi data session_state
if "barang" not in st.session_state:
    st.session_state.barang = pd.DataFrame(columns=["Nama", "Stok (pcs)", "Harga per pcs"])

if "penjualan" not in st.session_state:
    st.session_state.penjualan = pd.DataFrame(columns=["Tanggal", "Barang", "Jumlah", "Satuan", "Total (Rp)"])

if "keuangan_lain" not in st.session_state:
    st.session_state.keuangan_lain = pd.DataFrame(columns=["Tanggal", "Keterangan", "Masuk (Rp)", "Keluar (Rp)"])

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

# ---------------------- Tambah Barang ----------------------
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

        st.session_state.nama_barang = ""
        st.session_state.stok_barang = 0
        st.session_state.harga_barang = ""
        st.experimental_rerun()

st.subheader("📋 Daftar Barang")
df_display = st.session_state.barang.copy()
df_display["Harga per pcs"] = df_display["Harga per pcs"].apply(format_rupiah)
st.dataframe(df_display, use_container_width=True)

# ---------------------- Penjualan ----------------------
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
        st.session_state.barang.at[idx, "Stok (pcs)"] -= jumlah_pcs

        new_row = {
            "Tanggal": tgl.strftime("%Y-%m-%d"),
            "Barang": barang_pilihan,
            "Jumlah": jumlah,
            "Satuan": satuan,
            "Total (Rp)": total
        }
        st.session_state.penjualan = pd.concat([st.session_state.penjualan, pd.DataFrame([new_row])], ignore_index=True)
        st.success(f"Berhasil menjual {jumlah} {satuan} {barang_pilihan} (Rp {format_rupiah(total)})")

        st.session_state.jual_barang = st.session_state.barang["Nama"].iloc[0]
        st.session_state.jual_satuan = "pcs"
        st.session_state.jual_jumlah = 1
        st.experimental_rerun()

st.subheader("🗒️ Riwayat Penjualan")
if st.session_state.penjualan.empty:
    st.info("Belum ada penjualan.")
else:
    dfjual = st.session_state.penjualan.copy()
    dfjual["Total (Rp)"] = dfjual["Total (Rp)"].apply(format_rupiah)
    st.dataframe(dfjual, use_container_width=True)

    total_semua = st.session_state.penjualan["Total (Rp)"].sum()
    st.markdown(f"### 💰 Total Penjualan: Rp {format_rupiah(total_semua)}")

# ---------------------- Keuangan Harian ----------------------
st.header("➕ Tambah Catatan Keuangan Lain")
with st.form("form_keuangan"):
    tgl = st.date_input("Tanggal Keuangan", date.today())
    ket = st.text_input("Keterangan")
    masuk_str = st.text_input("Pemasukan (Rp)", value="0")
    keluar_str = st.text_input("Pengeluaran (Rp)", value="0")
    simpan = st.form_submit_button("Simpan")

if simpan:
    masuk = parse_rupiah(masuk_str)
    keluar = parse_rupiah(keluar_str)

    if not ket:
        st.error("Keterangan harus diisi.")
    else:
        new_data = {
            "Tanggal": tgl.strftime("%Y-%m-%d"),
            "Keterangan": ket,
            "Masuk (Rp)": masuk,
            "Keluar (Rp)": keluar
        }
        st.session_state.keuangan_lain = pd.concat(
            [st.session_state.keuangan_lain, pd.DataFrame([new_data])],
            ignore_index=True
        )
        st.success("Data keuangan berhasil disimpan.")
        st.experimental_rerun()

st.header("📊 Laporan Keuangan Harian")
tanggal_filter = st.date_input("Pilih Tanggal", date.today())

penjualan_today = st.session_state.penjualan
penjualan_today = penjualan_today[penjualan_today["Tanggal"] == tanggal_filter.strftime("%Y-%m-%d")]

keuangan_today = st.session_state.keuangan_lain
keuangan_today = keuangan_today[keuangan_today["Tanggal"] == tanggal_filter.strftime("%Y-%m-%d")]

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🧾 Penjualan")
    if penjualan_today.empty:
        st.info("Belum ada penjualan.")
    else:
        dfjual = penjualan_today.copy()
        dfjual["Total (Rp)"] = dfjual["Total (Rp)"].apply(format_rupiah)
        st.dataframe(dfjual, use_container_width=True)

        total_penjualan = penjualan_today["Total (Rp)"].sum()
        st.success(f"Total Penjualan: Rp {format_rupiah(total_penjualan)}")

with col2:
    st.markdown("#### 📒 Catatan Keuangan Lain")
    if keuangan_today.empty:
        st.info("Belum ada catatan.")
    else:
        dflake = keuangan_today.copy()
        dflake["Masuk (Rp)"] = dflake["Masuk (Rp)"].apply(format_rupiah)
        dflake["Keluar (Rp)"] = dflake["Keluar (Rp)"].apply(format_rupiah)
        st.dataframe(dflake, use_container_width=True)

        total_masuk = keuangan_today["Masuk (Rp)"].sum()
        total_keluar = keuangan_today["Keluar (Rp)"].sum()
        st.success(f"Total Masuk: Rp {format_rupiah(total_masuk)}")
        st.error(f"Total Keluar: Rp {format_rupiah(total_keluar)}")

if not penjualan_today.empty or not keuangan_today.empty:
    laba = total_penjualan + total_masuk - total_keluar
    st.markdown(f"### 💰 Laba Hari Ini: Rp {format_rupiah(laba)}")