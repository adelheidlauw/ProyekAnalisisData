import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul aplikasi
st.title("Analisis Kualitas Udara di Kota Wanliu")

# Membaca File
@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "PRSA_Data_Wanliu_20130301-20170228.csv")
    Wanliu_df= pd.read_csv(file_path)
    return Wanliu_df
Wanliu_df=load_data()

# Konversi tanggal
Wanliu_df['date'] = pd.to_datetime(Wanliu_df[['year', 'month', 'day', 'hour']])
    
# Sidebar untuk filter PM2.5 dan PM10
st.sidebar.header("Filter Data")
pm25_range = st.sidebar.slider("PM2.5 Range", float(Wanliu_df['PM2.5'].min()), float(df['PM2.5'].max()), (float(df['PM2.5'].min()), float(df['PM2.5'].max())))
pm10_range = st.sidebar.slider("PM10 Range", float(Wanliu_df['PM10'].min()), float(df['PM10'].max()), (float(df['PM10'].min()), float(df['PM10'].max())))
    
# Filter data
df_filtered = Wanliu_df[(df['PM2.5'] >= pm25_range[0]) & (Wanliu_df['PM2.5'] <= pm25_range[1]) &
                    (Wanliu_df['PM10'] >= pm10_range[0]) & (Wanliu_df['PM10'] <= pm10_range[1])]
    
# Tampilkan data
st.subheader("Dataset yang difilter")
st.write(df_filtered.head())
    
# Visualisasi rata-rata PM2.5 dan PM10 per bulan
monthly_mean = df_filtered.groupby('month')[['PM2.5', 'PM10']].mean().reset_index()
fig, ax = plt.subplots()
sns.lineplot(data=monthly_mean, x='month', y='PM2.5', label='PM2.5', marker='o')
sns.lineplot(data=monthly_mean, x='month', y='PM10', label='PM10', marker='s')
ax.set_title("Rata-rata PM2.5 dan PM10 per Bulan")
ax.set_xlabel("Bulan")
ax.set_ylabel("Konsentrasi")
st.pyplot(fig)

# Heatmap Korelasi
st.subheader("Heatmap Korelasi")
fig, ax = plt.subplots()
sns.heatmap(df_filtered[['PM2.5', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].corr(), annot=True, cmap='coolwarm')
st.pyplot(fig)
