import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Judul Aplikasi
st.set_page_config(page_title="Jurnal Guru SMAN 24", layout="centered")
st.title("📓 Jurnal Pembelajaran Guru")
st.subheader("SMAN 24 Kabupaten Tangerang")

# Koneksi ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Form Input
with st.form(key="jurnal_form"):
    col1, col2 = st.columns(2)
    with col1:
        hari = st.selectbox("Hari", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"])
        tanggal = st.date_input("Tanggal")
    with col2:
        jam_ke = st.text_input("Jam Ke")
        kelas = st.text_input("Kelas")
    
    materi = st.text_area("Materi Pembelajaran")
    
    c1, c2 = st.columns(2)
    with c1:
        hadir = st.number_input("Hadir", min_value=0, step=1)
    with c2:
        tidak_hadir = st.text_input("Tidak Hadir")
        
    keterangan = st.text_input("Keterangan")
    submit = st.form_submit_button("Simpan Data Jurnal")

# Logika Simpan Data
if submit:
    try:
        # 1. Ambil data lama
        df_lama = conn.read(worksheet="Sheet1", ttl=0)
        
        # 2. Buat data baru dalam format teks agar tidak error
        data_baru = pd.DataFrame([{
            "Hari": str(hari),
            "Tanggal": str(tanggal),
            "Jam Ke": str(jam_ke),
            "Kelas": str(kelas),
            "Materi": str(materi),
            "Hadir": str(hadir),
            "Tidak Hadir": str(tidak_hadir),
            "Keterangan": str(keterangan)
        }])
        
        # 3. Gabungkan data
        if df_lama.empty:
            df_akhir = data_baru
        else:
            df_akhir = pd.concat([df_lama, data_baru], ignore_index=True)
        
        # 4. Kirim ke Google Sheets
        conn.update(worksheet="Sheet1", data=df_akhir)
        
        st.success("Alhamdulillah! Data berhasil terkirim ke Google Sheets.")
        st.balloons()
        
    except Exception as e:
        st.error(f"Koneksi Bermasalah: {e}")
        st.info("Pastikan link di Secrets berakhiran /edit?usp=sharing")
