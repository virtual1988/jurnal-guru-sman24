import streamlit as st
import requests
import json

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Jurnal Guru SMAN 24", layout="centered")

# 2. Judul Aplikasi
st.title("📓 Jurnal Pembelajaran Guru")
st.subheader("SMAN 24 Kabupaten Tangerang")
st.write("Selamat Datang, Pak Budiarto. Data akan langsung tersimpan ke Google Sheets.")

# 3. URL Jembatan (Apps Script)
URL_APP_SCRIPT = "https://script.google.com/macros/s/AKfycbw_hFSoHUHFQlA_2Z3478OYJra3BtCWTyoHuJ4IcjttmPSUBT8Ri8LA6USZf04aI4buKQ/exec"

# 4. Membuat Form Inputan
with st.form(key="jurnal_form", clear_on_submit=True):
    st.markdown("### Form Input Jurnal")
    col1, col2 = st.columns(2)
    
    with col1:
        hari = st.selectbox("Hari", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"])
        tanggal = st.date_input("Tanggal")
    
    with col2:
        jam_ke = st.text_input("Jam Ke (Contoh: 1-3)")
        kelas = st.text_input("Kelas (Contoh: 10.1)")

    materi = st.text_area("Materi Pembelajaran")
    
    st.write("---")
    st.markdown("### Kehadiran & Keterangan")
    c1, c2 = st.columns(2)
    with c1:
        hadir = st.text_input("Jumlah Siswa Hadir(Sebutkan nama/jumlah)")
    with c2:
        tidak_hadir = st.text_input("Tidak Hadir (Sebutkan nama/jumlah)")

    keterangan = st.text_input("Keterangan", placeholder="Contoh: Terlaksana")

    submit_button = st.form_submit_button(label="🚀 Simpan Data")

# 5. Logika Pengiriman Data ke Google Sheets
if submit_button:
    if not materi or not kelas:
        st.error("Gagal: Materi dan Kelas wajib diisi!")
    else:
        # Menyiapkan paket data (Payload)
        payload = {
            "hari": hari,
            "tanggal": str(tanggal),
            "jam_ke": jam_ke,
            "kelas": kelas,
            "materi": materi,
            "hadir": hadir,
            "tidak_hadir": tidak_hadir,
            "keterangan": keterangan
        }
        
        try:
            with st.spinner('Sedang mengirim data...'):
                # Mengirim data ke Apps Script menggunakan metode POST
                response = requests.post(URL_APP_SCRIPT, data=json.dumps(payload))
                
            if response.status_code == 200:
                st.success(f"Alhamdulillah! Jurnal kelas {kelas} berhasil tersimpan.")
                st.balloons()
            else:
                st.error(f"Gagal mengirim. Kode Error: {response.status_code}")
                
        except Exception as e:
            st.error(f"Terjadi kesalahan koneksi: {e}")

# Footer
st.markdown("---")
st.caption("Digitalisasi Jurnal Guru Informatika - SMAN 24 Kab. Tangerang")
