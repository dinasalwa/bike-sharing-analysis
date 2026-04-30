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

# --- 2. LOAD DATA ---
@st.cache_data
def load_data():
    base_dir = os.path.dirname(__file__)
    day_path = os.path.join(base_dir, "day.csv")
    hour_path = os.path.join(base_dir, "hour.csv")
    
    day_df = pd.read_csv(day_path)
    hour_df = pd.read_csv(hour_path)
    
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    # Mapping Cuaca
    day_df['weathersit_label'] = day_df['weathersit'].map({
        1: 'Clear', 2: 'Misty/Cloudy', 3: 'Light Snow/Rain', 4: 'Severe Weather'
    })

    # Manual Grouping Kategori Waktu
    def get_time_category(hour):
        if 5 <= hour < 12: return "Pagi"
        elif 12 <= hour < 17: return "Siang"
        elif 17 <= hour < 21: return "Sore"
        else: return "Malam"
    
    hour_df['time_category'] = hour_df['hr'].apply(get_time_category)
    
    return day_df, hour_df

day_df, hour_df = load_data()

# --- 3. SIDEBAR ---
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1507035895480-2b3156c31fc8?auto=format&fit=crop&q=80&w=2070", use_container_width=True)
    st.title("🚲 Bike Sharing Analysis")
    
    # FIX VALUEERROR: Menangani pemilihan rentang waktu agar tidak eror saat baru klik 1 tanggal
    date_range = st.date_input(
        label='Rentang Waktu:',
        min_value=day_df["dteday"].min(),
        max_value=day_df["dteday"].max(),
        value=[day_df["dteday"].min(), day_df["dteday"].max()]
    )
    
    st.markdown("---")
    st.write("**Dashboard ini digunakan untuk memantau performa harian penyewaan sepeda berdasarkan dataset 'Bike Sharing'.**")
    st.info("**Gunakan filter tanggal di atas untuk melihat data pada periode tertentu.**")

# Pastikan start_date dan end_date terdefinisi dengan benar
if isinstance(date_range, list) or isinstance(date_range, tuple):
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = date_range[0]
        end_date = day_df["dteday"].max()
else:
    start_date = end_date = date_range

# --- 4. FILTER DATA ---
main_df = day_df[(day_df["dteday"] >= pd.to_datetime(start_date)) & (day_df["dteday"] <= pd.to_datetime(end_date))]
main_hour_df = hour_df[(hour_df["dteday"] >= pd.to_datetime(start_date)) & (hour_df["dteday"] <= pd.to_datetime(end_date))]

# --- 5. HEADER ---
st.title("Bike Sharing Performance Dashboard 📊")
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1: st.metric("Total Penyewaan", value=f"{main_df.cnt.sum():,}")
with col_m2: st.metric("Rata-rata Harian", value=f"{round(main_df.cnt.mean()):,}")
with col_m3: st.metric("Puncak Penyewaan", value=f"{main_df.cnt.max():,}")

st.divider()

# --- 6. VISUALISASI UTAMA ---

# TREN BULANAN
st.subheader("📈 Tren Pertumbuhan Penyewaan Sepeda")
monthly_rentals = main_df.resample(rule='ME', on='dteday').agg({"cnt": "sum"}).reset_index()
fig1, ax1 = plt.subplots(figsize=(12, 5))
ax1.plot(monthly_rentals["dteday"], monthly_rentals["cnt"], marker='o', linewidth=2, color="#72BCD4")
ax1.set_ylabel("Jumlah Penyewaan")
ax1.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig1)
with st.expander("Lihat Penjelasan Tren"):
    st.write("Grafik ini menunjukkan fluktuasi penyewaan dari bulan ke bulan. Penurunan atau kenaikan tajam biasanya dipengaruhi oleh faktor musiman (season) atau hari libur (holiday).")

st.divider()

# ANALISIS CUACA
st.subheader("☁️ Dampak Kondisi Cuaca Terhadap Penyewaan")
weather_data = main_df.groupby("weathersit_label")["cnt"].mean().sort_values(ascending=False).reset_index()
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(x="weathersit_label", y="cnt", data=weather_data, color="#72BCD4", ax=ax2)
ax2.set_xlabel("Kondisi Cuaca")
ax2.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig2)
with st.expander("Lihat Penjelasan Cuaca"):
    st.write("Data menunjukkan bahwa rata-rata penyewaan tertinggi terjadi pada cuaca **Clear/Cerah**. Sebaliknya, kondisi cuaca ekstrem seperti hujan lebat atau salju secara signifikan mengurangi minat pengguna untuk bersepeda.")

st.divider()

# HOURLY & TIME CATEGORY ANALYSIS (BERDAMPINGAN)
st.subheader("🕒 Hourly & Time Category Analysis")
col_v1, col_v2 = st.columns(2)

with col_v1:
    st.markdown("<p style='text-align: center; font-weight: bold;'>Pola Berdasarkan Jam</p>", unsafe_allow_html=True)
    hourly_data = main_hour_df.groupby("hr")["cnt"].mean().reset_index()
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    sns.lineplot(x="hr", y="cnt", data=hourly_data, marker='o', color="#72BCD4", ax=ax3)
    ax3.set_xticks(range(0, 24))
    ax3.set_xlabel("Jam (0-23)")
    ax3.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig3)

with col_v2:
    st.markdown("<p style='text-align: center; font-weight: bold;'>Pola Berdasarkan Kelompok Waktu</p>", unsafe_allow_html=True)
    category_data = main_hour_df.groupby("time_category")["cnt"].mean().reindex(["Pagi", "Siang", "Sore", "Malam"]).reset_index()
    fig4, ax4 = plt.subplots(figsize=(8, 6))
    # Menggunakan variasi tone warna biru agar mirip dengan referensi gambar kamu
    colors = ["#212121", "#455A64", "#78909C", "#90CAF9"]
    sns.barplot(x="time_category", y="cnt", data=category_data, palette=colors, ax=ax4)
    ax4.set_xlabel("Kategori Waktu")
    ax4.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig4)

st.info("Informasi: Analisis menunjukkan jam sibuk pada pagi hari (sekitar jam 8) dan sore hari (sekitar jam 17). Teknik *Manual Grouping* membagi waktu menjadi 4 kategori untuk mempermudah identifikasi perilaku pengguna.")

# --- 7. FOOTER ---
st.markdown("---")
st.caption('ID Dicoding: CDCC596D6X0981 | Copyright © Dina Salwa Mannatu 2026')
