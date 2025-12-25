import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Cek Nilai TKA", page_icon="🎓")

# 2. CSS untuk Kartu Nilai
st.markdown("""
<style>
    .card { background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 10px; }
    .nilai-besar { font-size: 32px; font-weight: bold; color: #1f77b4; text-align: center; }
    .label-predikat { font-size: 14px; color: #555; text-align: center; }
</style>
""", unsafe_allow_html=True)

# 3. Load Data Otomatis dari Repository
@st.cache_data
def load_data():
    nama_file = 'Hasil_TKA_Siswa_2025.xlsx - Sheet1.csv'
    try:
        # Membaca file langsung
        df = pd.read_csv(nama_file)
        # Pastikan kolom NISN menjadi text agar rapi
        df['NISN'] = df['NISN'].astype(str)
        return df
    except FileNotFoundError:
        return None

# Load data saat aplikasi mulai
df = load_data()

# ==========================================
# TAMPILAN UTAMA
# ==========================================

st.title("🎓 Portal Hasil TKA Siswa")
st.write("Masukkan nama siswa untuk melihat Kartu Hasil Studi.")

if df is not None:
    # --- PENCARIAN NAMA ---
    daftar_nama = sorted(df['Nama Peserta'].unique())
    selected_siswa = st.selectbox(
        "Cari Nama Siswa:", 
        options=daftar_nama, 
        index=None, 
        placeholder="Ketik nama siswa..."
    )

    # --- TAMPILAN HASIL ---
    if selected_siswa:
        # Ambil data satu baris milik siswa tersebut
        siswa = df[df['Nama Peserta'] == selected_siswa].iloc[0]

        st.divider()
        st.subheader(f"Hasil Studi: {siswa['Nama Peserta']}")
        
        # Info Dasar
        col_info1, col_info2 = st.columns(2)
        col_info1.info(f"**NISN:** {siswa['NISN']}")
        col_info2.info(f"**Nomor Peserta:** {siswa['Nomor Peserta']}")

        # Fungsi kecil untuk membuat kotak nilai
        def kartu_nilai(mapel, nilai, predikat):
            st.markdown(f"""
            <div class="card">
                <div style="text-align: center; font-weight: bold;">{mapel}</div>
                <div class="nilai-besar">{nilai}</div>
                <div class="label-predikat">Predikat: {predikat}</div>
            </div>
            """, unsafe_allow_html=True)

        # Baris 1: Mapel Wajib
        st.markdown("#### 📚 Mata Pelajaran Wajib")
        col1, col2, col3 = st.columns(3)
        with col1: kartu_nilai("Bahasa Indonesia", siswa['Nilai_B_Indo'], siswa['Pred_B_Indo'])
        with col2: kartu_nilai("Matematika", siswa['Nilai_MTK'], siswa['Pred_MTK'])
        with col3: kartu_nilai("Bahasa Inggris", siswa['Nilai_B_Ing'], siswa['Pred_B_Ing'])

        # Baris 2: Mapel Pilihan
        st.markdown("#### 🎯 Mata Pelajaran Pilihan")
        col_p1, col_p2 = st.columns(2)
        with col_p1: kartu_nilai(siswa['Pilihan1_Mapel'], siswa['Nilai_Pil1'], siswa['Pred_Pil1'])
        with col_p2: kartu_nilai(siswa['Pilihan2_Mapel'], siswa['Nilai_Pil2'], siswa['Pred_Pil2'])

else:
    # Pesan Error jika file Excel tidak ada di repository
    st.error("⚠️ File data tidak ditemukan!")
    st.warning("Pastikan file 'Hasil_TKA_Siswa_2025.xlsx - Sheet1.csv' sudah ada di folder yang sama dengan app.py")
