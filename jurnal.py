import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Judul Aplikasi
st.title("📓 Jurnal Pembelajaran Guru")
st.subheader("SMAN 24 Kabupaten Tangerang")
st.write("Selamat Datang, Pak Budiarto. Silakan isi jurnal di bawah ini.")

# 2. Inisialisasi Koneksi ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. Membuat Form Inputan
with st.form(key="jurnal_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        hari = st.selectbox("Hari", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"])
        tanggal = st.date_input("Tanggal")
    
    with col2:
        jam_ke = st.text_input("Jam Ke (Contoh: 1-3)")
        kelas = st.text_input("Kelas (Contoh: 10.1)")

    materi = st.text_area("Materi Pembelajaran")
    
    st.write("---")
    st.write("### Kehadiran Siswa")
    c1, c2 = st.columns(2)
    with c1:
        hadir = st.number_input("Hadir", min_value=0, step=1)
    with c2:
        tidak_hadir = st.text_input("Tidak Hadir (Gunakan '-' jika nihil)")

    # Kolom keterangan yang Bapak minta (input teks manual)
    keterangan = st.text_input("Keterangan", placeholder="Contoh: Terlaksana dengan baik / Materi selesai")

    submit_button = st.form_submit_button(label="Simpan Data")

# 4. Logika Pengiriman Data (Kode Sakti)
if submit_button:
    if not materi or not kelas:
        st.error("Mohon lengkapi Materi dan Kelas terlebih dahulu!")
    else:
        try:
            # Mengambil data lama untuk digabungkan dengan data baru
            existing_data = conn.read(worksheet="Sheet1", usecols=list(range(8)), ttl=0)
            
            # Membuat baris data baru dari inputan Bapak
            new_data = pd.DataFrame([{
                "Hari": hari,
                "Tanggal": str(tanggal),
                "Jam Ke": jam_ke,
                "Kelas": kelas,
                "Materi": materi,
                "Hadir": hadir,
                "Tidak Hadir": tidak_hadir,
                "Keterangan": keterangan
            }])

            # Menggabungkan data lama dan baru
            updated_df = pd.concat([existing_data, new_data], ignore_index=True)

            # Update kembali ke Google Sheets
            conn.update(worksheet="Sheet1", data=updated_df)
            
            st.success(f"Alhamdulillah! Jurnal kelas {kelas} berhasil disimpan.")
            st.balloons()
            
        except Exception as e:
            st.error(f"Terjadi kesalahan koneksi: {e}")
            st.info("Pastikan Google Sheet Anda sudah di-set 'Anyone with the link can EDIT'")
