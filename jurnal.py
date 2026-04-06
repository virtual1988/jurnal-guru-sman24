import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Jurnal Guru SMAN 24", layout="centered")

# 2. Judul Aplikasi
st.title("📓 Jurnal Pembelajaran Guru")
st.subheader("SMAN 24 Kabupaten Tangerang")
st.write("Selamat Datang, Pak Budiarto. Silakan isi jurnal di bawah ini.")

# 3. Inisialisasi Koneksi ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 4. Membuat Form Inputan
with st.form(key="jurnal_form"):
    st.markdown("### Masukkan Data Pembelajaran")
    col1, col2 = st.columns(2)
    
    with col1:
        hari = st.selectbox("Hari", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"])
        tanggal = st.date_input("Tanggal")
    
    with col2:
        jam_ke = st.text_input("Jam Ke (Contoh: 1-10)")
        kelas = st.text_input("Kelas (Contoh: 12.6)")

    materi = st.text_area("Materi Pembelajaran")
    
    st.write("---")
    st.markdown("### Kehadiran Siswa")
    c1, c2 = st.columns(2)
    with c1:
        hadir = st.number_input("Hadir", min_value=0, step=1)
    with c2:
        tidak_hadir = st.text_input("Tidak Hadir (Gunakan '-' jika nihil)")

    keterangan = st.text_input("Keterangan", placeholder="Contoh: Terlaksana / Remedial")

    submit_button = st.form_submit_button(label="Simpan Data Jurnal")

# 5. Logika Pengiriman Data (Sangat Stabil)
if submit_button:
    if not materi or not kelas:
        st.error("Waduh Pak, Materi dan Kelas jangan dikosongkan ya!")
    else:
        try:
            # Membaca data lama dan membersihkan spasi di nama kolom secara otomatis
            existing_data = conn.read(worksheet="Sheet1", ttl=0)
            existing_data.columns = existing_data.columns.str.strip()
            
            # Membuat baris data baru (Semua dipaksa jadi string/teks agar tidak Error 400)
            new_row = {
                "Hari": str(hari),
                "Tanggal": tanggal.strftime('%Y-%m-%d'),
                "Jam Ke": str(jam_ke),
                "Kelas": str(kelas),
                "Materi": str(materi),
                "Hadir": str(hadir),
                "Tidak Hadir": str(tidak_hadir),
                "Keterangan": str(keterangan)
            }
            new_data = pd.DataFrame([new_row])

            # Menggabungkan data lama dengan data baru
            updated_df = pd.concat([existing_data, new_data], ignore_index=True)

            # Update kembali ke Google Sheets
            conn.update(worksheet="Sheet1", data=updated_df)
            
            st.success(f"Alhamdulillah! Jurnal kelas {kelas} sudah tersimpan.")
            st.balloons()
            
        except Exception as e:
            st.error(f"Maaf Pak, ada kendala: {e}")
            st.info("Saran: Pastikan Baris 1 di Sheets sudah benar dan tidak ada spasi liar.")
