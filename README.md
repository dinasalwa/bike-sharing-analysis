# 🚲 Proyek Analisis Data: Bike Sharing Dataset

## Deskripsi
Proyek ini merupakan submission akhir untuk kelas **"Belajar Analisis Data dengan Python"** di Dicoding. Dashboard ini memberikan wawasan mendalam mengenai tren penyewaan sepeda berdasarkan parameter waktu, kondisi cuaca, dan pola jam harian pengguna.

---

## 👤 Identitas Pengembang
- **Nama:** Dina Salwa Mannatu
- **Email:** dinasalwa2105@gmail.com
- **ID Dicoding:** dina_salwa

---

## 📂 Struktur Direktori 
```text
.
├── dashboard/
│   ├── dashboard.py
│   ├── day.csv
│   └── hour.csv
├── data/
│   ├── day.csv
│   └── hour.csv
├── Proyek_Analisis_Data_Dina_Salwa_Mannatu.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## 🚀 Instalasi Lingkungan Kerja (Local)

**Setup Environment: Anaconda**
```
conda create --name bike-sharing-ds python=3.9
conda activate bike-sharing-ds
pip install -r requirements.txt
```

**Setup Environment: Shell/Terminal**
```
mkdir bike-sharing-analysis-main
cd bike-sharing-analysis-main
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 💻 Cara Menjalankan Dashboard
Setelah semua library terinstal, masuk ke direktori proyek dan jalankan perintah berikut:
```
cd dashboard
streamlit run dashboard.py
```

Atau jika dijalankan dari root folder:
```
python -m streamlit run dashboard/dashboard.py
```

## 🌐 Live Dashboard
Anda dapat mengakses dashboard yang telah di-deploy melalui tautan berikut:

👉 [Klik Di Sini untuk Melihat Dashboard](https://dina-bike-sharing-analysis.streamlit.app/)
