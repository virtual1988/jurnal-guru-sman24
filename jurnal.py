import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Jurnal Guru SMAN 24", layout="centered")

# URL Google Sheet Bapak
URL_SHEET = "https://docs.google.com/spreadsheets/d/1Yq1VujXXKKLXhm7J1PQKX23YJEV3T7Jzc2r1u0fpsBg/edit?usp=sharing"

# Membuat koneksi ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 2. TAMPILAN JUDUL ---
st.title("📓 Jurnal Pembelajaran Guru")
st.subheader("SMAN 24 Kabupaten Tangerang")
st.write("Selamat Datang, Pak Budiarto. Silakan isi jurnal di bawah ini.")

# --- 3. FORM INPUT JURNAL ---
with st.form(key="form_jurnal"):
    st.write("### Masukkan Data Pembelajaran")
    
    # Baris 1: Hari, Tanggal, Jam Ke
    col1, col2, col3 = st.columns(3)
    with col1:
        hari = st.selectbox("Hari", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"])
    with col2:
        tanggal = st.date_input("Tanggal")
    with col3:
        jam_ke = st.text_input("Jam Ke (Contoh: 3-4)")

    # Baris 2: Kelas dan Materi
    kelas = st.text_input("Kelas (Contoh: 12.9)")
    materi = st.text_area("Materi Pembelajaran")

    # Baris 3: Kehadiran Siswa
    st.write("**Kehadiran Siswa**")
    col_hadir, col_tidak = st.columns(2)
    with col_hadir:
        hadir = st.number_input("Hadir", min_value=0, step=1)
    with col_tidak:
        tidak_hadir = st.text_input("Tidak Hadir (Gunakan '-' jika nihil)", value="-")

    # Baris 4: Keterangan (Sudah Input Teks Manual)
    keterangan = st.text_input("Keterangan", placeholder="Contoh: Terlaksana dengan baik / Materi selesai")
    
    # Tombol Simpan (Harus sejajar dengan 'keterangan')
    submit_button = st.form_submit_button(label="Simpan")

# --- 4. LOGIKA PENYIMPANAN DATA ---
if submit_button:
    if kelas == "" or materi == "":
        st.error("Gagal! Kolom Kelas dan Materi wajib diisi.")
    else:
        try:
            # Membaca data yang sudah ada
            existing_data = conn.read(spreadsheet=URL_SHEET)
            
            # Membuat baris data baru
            new_record = pd.DataFrame([{
                "Hari": hari,
                "Tanggal": str(tanggal),
                "Jam Ke": jam_ke,
                "Kelas": kelas,
                "Materi": materi,
                "Hadir": hadir,
                "Tidak Hadir": tidak_hadir,
                "Keterangan": keterangan
            }])
            
            # Menggabungkan data
            updated_df = pd.concat([existing_data, new_record], ignore_index=True)
            
            # Update kembali ke Google Sheets
            conn.update(spreadsheet=URL_SHEET, data=updated_df)
            
            st.success(f"Alhamdulillah! Jurnal kelas {kelas} berhasil disimpan.")
            st.balloons()
            
        except Exception as e:
            st.error(f"Terjadi kesalahan koneksi: {e}")
            st.info("Pastikan Google Sheet Anda sudah di-set 'Anyone with the link can EDIT'")