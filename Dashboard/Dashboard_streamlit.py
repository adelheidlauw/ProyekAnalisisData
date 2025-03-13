import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ------------------------------
# 📌 Judul Aplikasi
st.title("📊 Analisis Polusi Udara - Kota Wanliu 📊")

# ------------------------------
# Membaca File
@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "PRSA_Data_Wanliu_20130301-20170228.csv")
    Wanliu_df = pd.read_csv(file_path)
    return Wanliu_df

Wanliu_df = load_data()

# ------------------------------
# Sidebar untuk Filter Data
st.sidebar.header("🔍 Filter Data")

# **Filter berdasarkan tanggal**
Wanliu_df['date'] = pd.to_datetime(Wanliu_df[['year', 'month', 'day', 'hour']])
min_date, max_date = Wanliu_df['date'].min(), Wanliu_df['date'].max()
start_date = st.sidebar.date_input("Tanggal Mulai", min_date)
end_date = st.sidebar.date_input("Tanggal Akhir", max_date)

# **Filter berdasarkan bulan tertentu**
bulan = Wanliu_df['month'].unique()
bulan_pilihan = st.sidebar.multiselect("Pilih Bulan", bulan, default=bulan)

# **Filter berdasarkan variabel**
kolom_numerik = ['PM2.5', 'PM10', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
kolom_pilihan = st.sidebar.multiselect("Pilih Variabel untuk Analisis", kolom_numerik, default=['PM2.5', 'PM10'])

# Terapkan filter ke DataFrame
filtered_df = Wanliu_df[
    (Wanliu_df['date'] >= pd.to_datetime(start_date)) & 
    (Wanliu_df['date'] <= pd.to_datetime(end_date)) & 
    (Wanliu_df['month'].isin(bulan_pilihan))
]

# ------------------------------
# Menampilkan Data Awal setelah Filter
st.subheader("📌 Data Awal setelah Filter")
st.write(filtered_df[kolom_pilihan].head())

# ------------------------------
# Mengecek Missing Values
st.subheader("📌 Cek Missing Values")
missing_values = filtered_df[kolom_pilihan].isnull().sum()
st.write(missing_values)

# ------------------------------
# Cleaning Data
st.subheader("📌 Cleaning Data")

# Hapus nilai Inf dan NaN
filtered_df = filtered_df.replace([float('inf'), float('-inf')], None).dropna()

# Cek ulang Missing Values setelah cleaning
cleaned_missing_values = filtered_df[kolom_pilihan].isnull().sum()
st.write("Jumlah nilai NaN setelah pembersihan:")
st.write(cleaned_missing_values)

# ------------------------------
# Deteksi Outlier dengan IQR
st.subheader("📌 Deteksi dan Pembersihan Outlier")

Q1 = filtered_df[kolom_pilihan].quantile(0.25)
Q3 = filtered_df[kolom_pilihan].quantile(0.75)
IQR = Q3 - Q1

batas_bawah = Q1 - 1.5 * IQR
batas_atas = Q3 + 1.5 * IQR

clean_df = filtered_df[~((filtered_df[kolom_pilihan] < batas_bawah) | (filtered_df[kolom_pilihan] > batas_atas)).any(axis=1)]

# Cek jumlah data sebelum dan sesudah
st.write(f"Jumlah data sebelum pembersihan: {filtered_df.shape[0]}")
st.write(f"Jumlah data setelah pembersihan: {clean_df.shape[0]}")

# ------------------------------
# Exploratory Data Analysis (EDA)
st.subheader("📌 Exploratory Data Analysis (EDA)")

# Hitung rata-rata PM2.5 dan PM10 per bulan setelah filter
monthly_mean = clean_df.groupby('month')[kolom_pilihan].mean().reset_index()

# Korelasi antar variabel yang dipilih
korelasi = clean_df[kolom_pilihan].corr()

# ------------------------------
# Visualisasi Tren Musiman PM2.5 & PM10
st.subheader("📊 Tren Musiman Berdasarkan Filter")

fig, ax = plt.subplots(figsize=(12, 6))
for col in kolom_pilihan:
    sns.lineplot(x=monthly_mean['month'], y=monthly_mean[col], label=col, marker='o', ax=ax)

ax.set_xlabel('Bulan')
ax.set_ylabel('Konsentrasi Polutan')
ax.set_title('Tren Musiman Berdasarkan Filter')
ax.legend()
ax.grid(True)
st.pyplot(fig)

# ------------------------------
# Heatmap Korelasi
st.subheader("📊 Korelasi antara Variabel yang Dipilih")

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(korelasi, annot=True, cmap='coolwarm', ax=ax)
ax.set_title('Korelasi antara Variabel yang Dipilih')
st.pyplot(fig)

# ------------------------------
# Kesimpulan
st.subheader("📌 Kesimpulan")
st.write("""
- Pengguna dapat menyesuaikan rentang waktu dan bulan untuk melihat pola polusi berdasarkan musim.
- Pemilihan variabel memungkinkan analisis lebih fleksibel terhadap faktor lingkungan.
- Heatmap korelasi memperlihatkan hubungan antara PM2.5, PM10, dan faktor lainnya secara lebih interaktif.
""")
