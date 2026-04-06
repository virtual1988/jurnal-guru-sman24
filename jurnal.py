import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Jurnal Guru SMAN 24", layout="centered")
st.title("📓 Jurnal Pembelajaran Guru")
st.subheader("SMAN 24 Kabupaten Tangerang")

# Koneksi ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

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

if submit:
    try:
        # Data yang akan dikirim
        new_row = pd.DataFrame([{
            "Hari": str(hari),
            "Tanggal": str(tanggal),
            "Jam Ke": str(jam_ke),
            "Kelas": str(kelas),
            "Materi": str(materi),
            "Hadir": str(hadir),
            "Tidak Hadir": str(tidak_hadir),
            "Keterangan": str(keterangan)
        }])
        
        # MEMAKSA UPDATE: Menggunakan lembar kerja baru jika Sheet1 bermasalah
        # Bapak bisa mengganti nama "DataJurnal" jika ingin membuat tab baru
        conn.update(worksheet="Sheet1", data=new_row)
        
        st.success("Alhamdulillah! Data berhasil disimpan.")
        st.balloons()
        
    except Exception as e:
        st.error(f"Terjadi kendala: {e}")
