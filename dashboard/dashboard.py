import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Bike Sharing Dashboard 🚲",
    layout="wide"
)

# --- 2. CUSTOM CSS ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    [data-testid="stMetricValue"] {
        font-size: 28px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOAD DATA ---
@st.cache_data
def load_data():
    base_dir = os.path.dirname(__file__)
    day_path = os.path.join(base_dir, "day.csv")
    hour_path = os.path.join(base_dir, "hour.csv")
    
    day_df = pd.read_csv(day_path)
    hour_df = pd.read_csv(hour_path)
    
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    # Mapping Cuaca agar tampilan lebih manusiawi
    day_df['weathersit'] = day_df['weathersit'].map({
        1: 'Clear', 2: 'Misty/Cloudy', 3: 'Light Snow/Rain', 4: 'Severe Weather'
    })
    return day_df, hour_df

day_df, hour_df = load_data()

# --- 4. SIDEBAR (Kalimat & Filter Tetap Ada) ---
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1507035895480-2b3156c31fc8?auto=format&fit=crop&q=80&w=2070", use_container_width=True)
    st.title("🚲 Bike Sharing Analysis")
    
    # Filter Rentang Waktu
    start_date, end_date = st.date_input(
        label='Pilih Rentang Waktu:',
        min_value=day_df["dteday"].min(),
        max_value=day_df["dteday"].max(),
        value=[day_df["dteday"].min(), day_df["dteday"].max()]
    )
    
    st.markdown("---")
    # Kalimat di sidebar yang kamu minta tetap ada
    st.write("**Deskripsi Proyek:**")
    st.write("Dashboard ini digunakan untuk memantau performa harian penyewaan sepeda berdasarkan dataset 'Bike Sharing'.")
    st.info("Gunakan filter tanggal di atas untuk melihat data pada periode tertentu.")

# Filter Data berdasarkan input sidebar
main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                 (day_df["dteday"] <= str(end_date))]

# --- 5. HEADER & RINGKASAN METRIK ---
st.title("Bike Sharing Performance Dashboard 📊")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", value=f"{main_df.cnt.sum():,}")
with col2:
    st.metric("Rata-rata Harian", value=f"{round(main_df.cnt.mean()):,}")
with col3:
    st.metric("Puncak Penyewaan", value=f"{main_df.cnt.max():,}")

st.divider()

# --- 6. TATA LETAK TAB ---
tab1, tab2, tab3 = st.tabs(["📈 Tren Bulanan", "☁️ Analisis Cuaca", "🕒 Pola Jam"])

# --- TAB 1: TREN BULANAN ---
with tab1:
    st.subheader("Visualisasi 1: Tren Pertumbuhan Penyewaan")
    # Perbaikan rule 'ME' (Month End) untuk pandas terbaru
    monthly_rentals = main_df.resample(rule='ME', on='dteday').agg({"cnt": "sum"}).reset_index()

    fig1, ax1 = plt.subplots(figsize=(16, 8))
    ax1.plot(monthly_rentals["dteday"], monthly_rentals["cnt"], marker='o', linewidth=3, color="#72BCD4")
    ax1.set_title("Total Penyewaan per Bulan (2011-2012)", fontsize=20)
    ax1.set_ylabel("Jumlah Penyewa")
    ax1.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig1)
    
    # Insight di bawah visualisasi
    with st.container():
        st.write("### 💡 Insight Tren Bulanan")
        st.write("- Terlihat adanya tren kenaikan penyewaan yang signifikan terutama memasuki tahun 2012.")
        st.write("- Penurunan musiman terlihat di akhir tahun, yang kemungkinan besar dipengaruhi faktor cuaca dingin.")

# --- TAB 2: ANALISIS CUACA ---
with tab2:
    st.subheader("Visualisasi 2: Dampak Kondisi Cuaca")
    weather_data = main_df.groupby("weathersit")["cnt"].mean().reset_index()

    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.barplot(x="weathersit", y="cnt", data=weather_data, palette="viridis", ax=ax2)
    ax2.set_title("Rata-rata Penyewaan Berdasarkan Cuaca", fontsize=18)
    ax2.set_xlabel(None)
    st.pyplot(fig2)
    
    with st.container():
        st.write("### 💡 Insight Analisis Cuaca")
        st.write("- Kondisi cuaca **Clear/Cerah** mendominasi jumlah rata-rata penyewaan harian.")
        st.write("- Sebaliknya, kondisi hujan atau salju ringan mengurangi minat pengguna secara drastis.")

# --- TAB 3: POLA JAM (Visualisasi ke-3) ---
with tab3:
    st.subheader("Visualisasi 3: Pola Jam Operasional")
    hourly_data = hour_df.groupby("hr")["cnt"].mean().reset_index()

    fig3, ax3 = plt.subplots(figsize=(14, 6))
    sns.lineplot(x="hr", y="cnt", data=hourly_data, marker='o', color="#D47272", linewidth=2)
    ax3.set_xticks(range(0, 24))
    ax3.set_title("Rata-rata Penyewaan Berdasarkan Jam dalam Sehari", fontsize=18)
    ax3.set_xlabel("Jam (0-23)")
    ax3.grid(True, alpha=0.3)
    st.pyplot(fig3)
    
    with st.container():
        st.write("### 💡 Insight Pola Jam")
        st.write("- Terjadi dua lonjakan utama pada jam sibuk, yaitu pukul **08:00** dan **17:00**.")
        st.write("- Hal ini mengindikasikan bahwa sepeda banyak digunakan oleh pekerja atau pelajar sebagai alat transportasi rutin.")

# --- 7. FOOTER ---
st.markdown("---")
st.caption('Copyright © Dina Salwa Mannatu | Proyek Analisis Data 2026')