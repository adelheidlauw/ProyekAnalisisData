import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ------------------------------
# Judul Aplikasi
st.title("Analisis Polusi Udara - Kota Wanliu")

# ------------------------------
# Membaca file
@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "PRSA_Data_Wanliu_20130301-20170228.csv")
    Wanliu_df= pd.read_csv(file_path)
    return Wanliu_df
Wanliu_df=load_data()

# ------------------------------
# Mengecek Missing Values
missing_values = Wanliu_df.isnull().sum()


# ------------------------------
# Konversi ke datetime
Wanliu_df['date'] = pd.to_datetime(Wanliu_df[['year', 'month', 'day', 'hour']])

# Hapus nilai Inf dan NaN
X = Wanliu_df[['TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']]
y = Wanliu_df['PM2.5']
    
X = X.replace([float('inf'), float('-inf')], None).dropna()
y = y.loc[X.index]

# Cek ulang Missing Values setelah cleaning
cleaned_missing_values = X.isnull().sum()

# ------------------------------
# Deteksi Outlier dengan IQR
    
Q1 = Wanliu_df[['PM2.5', 'PM10']].quantile(0.25)
Q3 = Wanliu_df[['PM2.5', 'PM10']].quantile(0.75)
IQR = Q3 - Q1

batas_bawah = Q1 - 1.5 * IQR
batas_atas = Q3 + 1.5 * IQR

Wanliu_clean_df = Wanliu_df[~((Wanliu_df[['PM2.5', 'PM10']] < batas_bawah) | (Wanliu_df[['PM2.5', 'PM10']] > batas_atas)).any(axis=1)]

# ------------------------------
# Exploratory Data Analysis (EDA)

# Hitung rata-rata PM2.5 dan PM10 per bulan
monthly_mean = Wanliu_clean_df.groupby('month')[['PM2.5', 'PM10']].mean().reset_index()

# Korelasi antar variabel
korelasi = Wanliu_clean_df[['PM2.5', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].corr()

# ------------------------------
# Visualisasi Tren Musiman PM2.5 & PM10
st.subheader("Tren Musiman PM2.5 dan PM10")

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x=monthly_mean['month'], y=monthly_mean['PM2.5'], label='PM2.5', marker='o', ax=ax)
sns.lineplot(x=monthly_mean['month'], y=monthly_mean['PM10'], label='PM10', marker='s', ax=ax)

ax.set_xlabel('Bulan')
ax.set_ylabel('Konsentrasi Polutan')
ax.set_title('Tren Musiman PM2.5 dan PM10 di Kota Wanliu')
ax.legend()
ax.grid(True)
st.pyplot(fig)

st.subheader("Penjelasan")
st.write("""
- Polusi udara mengalami fluktuasi musiman, dengan tingkat PM2.5 dan PM10 lebih tinggi pada bulan-bulan tertentu.
""")

# ------------------------------
# Heatmap Korelasi
st.subheader("Korelasi antara PM2.5 dan Faktor-Faktor Lingkungan")

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(korelasi, annot=True, cmap='coolwarm', ax=ax)
ax.set_title('Korelasi antara PM2.5 dan Faktor-Faktor Lain')
st.pyplot(fig)

# ------------------------------
# Kesimpulan
st.subheader("Penjelasan")
st.write("""
- Faktor utama yang mempengaruhi PM2.5 adalah suhu udara (TEMP), curah hujan (RAIN), dan kecepatan angin (WSPM).
- Suhu memiliki korelasi negatif dengan PM2.5, artinya saat suhu meningkat, tingkat polusi menurun.
- Curah hujan dan kecepatan angin membantu mengurangi polusi dengan menyebarkan atau membersihkan partikel dari udara.
""")