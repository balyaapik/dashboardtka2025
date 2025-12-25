import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="Dashboard TKA Siswa 2025",
    page_icon="🎓",
    layout="wide"
)

# Judul Utama
st.title("🎓 Dashboard Hasil TKA Siswa 2025")
st.markdown("---")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    try:
        # Mencoba membaca file CSV default
        df = pd.read_csv('Hasil_TKA_Siswa_2025.xlsx - Sheet1.csv')
        return df
    except FileNotFoundError:
        return None

df = load_data()

# Sidebar untuk Upload jika file tidak ditemukan atau ingin ganti file
with st.sidebar:
    st.header("Pengaturan Data")
    uploaded_file = st.file_uploader("Upload File CSV Hasil TKA", type=['csv'])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    
    if df is not None:
        st.success(f"Data dimuat: {len(df)} siswa")
    else:
        st.warning("Silakan upload file CSV atau pastikan file ada di folder yang sama.")
        st.stop()

# --- TABS MENU ---
tab1, tab2, tab3 = st.tabs(["📊 Statistik Sekolah", "👤 Detail Siswa", "📋 Data Mentah"])

# === TAB 1: STATISTIK ===
with tab1:
    st.header("Ringkasan Statistik Sekolah")
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Siswa", len(df))
    with col2:
        st.metric("Rata-rata B. Indo", f"{df['Nilai_B_Indo'].mean():.2f}")
    with col3:
        st.metric("Rata-rata Matematika", f"{df['Nilai_MTK'].mean():.2f}")
    with col4:
        st.metric("Rata-rata B. Inggris", f"{df['Nilai_B_Ing'].mean():.2f}")
    
    st.markdown("---")
    
    # Grafik Distribusi Predikat
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.subheader("Sebaran Predikat Bahasa Indonesia")
        fig_indo = px.bar(df['Pred_B_Indo'].value_counts().reset_index(), 
                          x='index', y='Pred_B_Indo', 
                          labels={'index': 'Predikat', 'Pred_B_Indo': 'Jumlah Siswa'},
                          color='index')
        st.plotly_chart(fig_indo, use_container_width=True)
        
    with col_g2:
        st.subheader("Sebaran Pilihan Mapel 1")
        fig_mapel1 = px.pie(df, names='Pilihan1_Mapel', title='Proporsi Pilihan Mata Pelajaran 1')
        st.plotly_chart(fig_mapel1, use_container_width=True)

# === TAB 2: DETAIL SISWA ===
with tab2:
    st.header("Cari Data Siswa")
    
    # Pilihan Siswa
    nama_siswa_list = df['Nama Peserta'].unique().tolist()
    selected_siswa = st.selectbox("Pilih Nama Siswa:", sorted(nama_siswa_list))
    
    # Filter Data
    student_data = df[df['Nama Peserta'] == selected_siswa].iloc[0]
    
    # Tampilan Kartu Hasil Studi
    st.markdown(f"### Hasil Studi: {student_data['Nama Peserta']}")
    
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.info(f"**NISN:** {student_data['NISN']}")
        st.write(f"**Nomor Peserta:** {student_data['Nomor Peserta']}")
    with col_info2:
        st.info(f"**TTL:** {student_data['TTL']}")
    
    st.markdown("#### Nilai Mata Pelajaran Wajib")
    col_w1, col_w2, col_w3 = st.columns(3)
    
    with col_w1:
        st.markdown(f"**Bahasa Indonesia**")
        st.markdown(f"## {student_data['Nilai_B_Indo']}")
        st.caption(f"Predikat: {student_data['Pred_B_Indo']}")
        
    with col_w2:
        st.markdown(f"**Matematika**")
        st.markdown(f"## {student_data['Nilai_MTK']}")
        st.caption(f"Predikat: {student_data['Pred_MTK']}")
        
    with col_w3:
        st.markdown(f"**Bahasa Inggris**")
        st.markdown(f"## {student_data['Nilai_B_Ing']}")
        st.caption(f"Predikat: {student_data['Pred_B_Ing']}")
        
    st.markdown("#### Nilai Mata Pelajaran Pilihan")
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        st.markdown(f"**{student_data['Pilihan1_Mapel']}** (Pilihan 1)")
        st.markdown(f"## {student_data['Nilai_Pil1']}")
        st.caption(f"Predikat: {student_data['Pred_Pil1']}")
        
    with col_p2:
        st.markdown(f"**{student_data['Pilihan2_Mapel']}** (Pilihan 2)")
        st.markdown(f"## {student_data['Nilai_Pil2']}")
        st.caption(f"Predikat: {student_data['Pred_Pil2']}")

# === TAB 3: DATA MENTAH ===
with tab3:
    st.header("Database Seluruh Siswa")
    st.dataframe(df, use_container_width=True)
