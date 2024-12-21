import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import gdown
sns.set(style='dark')

#Helper function untuk membuat beberapa dataframe
def sewa_permusim(df):
    sewa_permusim_df = df.groupby('season').agg({
        'casual': 'sum',
        'registered': 'sum',
        'cnt': 'sum'
    }).reset_index()
    return sewa_permusim_df

def sewa_workingday(df):
    casual_workingday = df.groupby('workingday').agg({
        'casual': 'mean',
    }).reset_index()

    registered_workingday = df.groupby('workingday').agg({
        'registered': 'mean',
    }).reset_index()
    
    total_workingday = df.groupby('workingday').agg({
        'cnt': 'mean',
    }).reset_index()

    return casual_workingday, registered_workingday, total_workingday

def sewa_perjam(df):
    bike_perhour = df.groupby('hr').agg({
        'casual': 'mean',
        'registered': 'mean',
        'cnt': 'mean'
    }).reset_index()
    return bike_perhour

def temperatur_total(df):
    temperatur = [0, 0.3, 0.7, 1]
    label_temperatur = ['Rendah', 'Sedang', 'Tinggi']
    df['temp_binned'] = pd.cut(day_df['temp'], bins=temperatur, labels=label_temperatur)

    temperatur_df = df.groupby('temp_binned').agg({
        'cnt': 'mean',
    }).reset_index()
    
    return temperatur_df

#Memuat data
file_id = "1j5y3UHZUC9TKMu3wsulL6vaAasYytS7a"
url = f'https://drive.google.com/uc?id={file_id}'
output = 'day.csv'
gdown.download(url, output, quiet=False)
day_df = pd.read_csv('day.csv')

file_id1 = "1fMy2FB0tFqpFer0OPoT6mIGZkGMh_JHL"
url = f'https://drive.google.com/uc?id={file_id1}'
output2 = 'hour.csv'
gdown.download(url, output2, quiet=False)
hour_df = pd.read_csv('hour.csv')

#Menyiapkan dataframe
sewa_permusim_df = sewa_permusim(day_df)
casual_workingday, registered_workingday, total_workingday = sewa_workingday(day_df)
sewa_perjam_df = sewa_perjam(hour_df)
temperatur_df = temperatur_total(day_df)

#Membuat dashboard
st.header('Dicoding Project Dashboard :sparkles:')

st.subheader('Pengaruh musim pada penyewaan sepeda')

fig, ax = plt.subplots(1, 2, figsize=(16,8))

#Membuat diagram batang untuk kategori 'kasual' dan 'registered'
sewa_permusim_df[['season', 'casual', 'registered']].plot(x='season', kind='bar', ax=ax[0], stacked=False)
ax[0].set_title('Jumlah Penyewaan Sepeda \'Casual\' dan \'Registered\' per Musim')
ax[0].set_xlabel('Musim')
ax[0].set_ylabel('Jumlah Penyewaan')
ax[0].set_xticks([0, 1, 2, 3])
ax[0].set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'], rotation=0)
ax[0].legend(['casual','registered'])

#Membuat diagram batang untuk total penyewaan
sewa_permusim_df[['season', 'cnt']].plot(x='season', kind='bar', ax=ax[1], stacked=False)
ax[1].set_title('Jumlah Penyewaan Sepeda per Musim')
ax[1].set_xlabel('Musim')
ax[1].set_ylabel('Jumlah Penyewaan')
ax[1].set_xticks([0, 1, 2, 3])
ax[1].set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'], rotation=0)
ax[1].legend(['Total'])

st.pyplot(fig)

st.markdown("""
Pada diagram batang diatas dapat terlihat bahwa musim gugur memiliki penyewaan yang terbanyak pada kategori kasual dan terdaftar (registered).  Sedangkan musim semi memiliki penyewaan paling sedikit pada kedua kategori.

Pada diagram batang diatas juga dapat terlihat bahwa musim gugur memiliki total penyewaan yang terbanyak. Sedangkan musim semi memiliki total penyewaan paling sedikit.
""")

st.subheader('Perbedaan tingkat penyewaan sepeda pada hari kerja dan hari libur')

fig1, axs = plt.subplots(2, 2, figsize=(12, 6))

#Membuat diagram batang perbedaan hari libur dan hari kerja pada kategori 'casual'
axs[0, 0].bar(['Hari Libur', 'Hari Kerja'], casual_workingday['casual'])
axs[0, 0].set_title('Rata-rata Penyewaan Sepeda Casual pada Hari Kerja dan Hari Libur')
axs[0, 0].set_xlabel('Tipe Hari')
axs[0, 0].set_ylabel('Rata-rata Penyewaan')

#Membuat diagram batang perbedaan hari libur dan hari kerja pada kategori 'registered'
axs[0, 1].bar(['Hari Libur', 'Hari Kerja'], registered_workingday['registered'])
axs[0, 1].set_title('Rata-rata Penyewaan Sepeda Registered pada Hari Kerja dan Hari Libur')
axs[0, 1].set_xlabel('Tipe Hari')
axs[0, 1].set_ylabel('Rata-rata Penyewaan')

#Membuat diagram batang perbedaan hari libur dan hari kerja
axs[1, 0].bar(['Hari Libur', 'Hari Kerja'], total_workingday['cnt'])
axs[1, 0].set_title('Rata-rata Total Penyewaan Sepeda pada Hari Kerja dan Hari Libur')
axs[1, 0].set_xlabel('Tipe Hari')
axs[1, 0].set_ylabel('Rata-rata Penyewaan')

fig1.delaxes(axs[1, 1])
plt.tight_layout()
st.pyplot(fig1)

st.markdown("""
Pada grafik di atas, kategori kasual memiliki jumlah rata-rata penyewaan lebih banyak di hari libur, sedangkan kategori terdaftar (registered) sebaliknya. Rata-rata total penyewaan sepeda lebih banyak pada hari kerja.
""")

st.subheader('Perbedaan tingkat penyewaan sepeda pada setiap jam')

fig, axs = plt.subplots(2, 2, figsize=(12, 6))

#Membuat diagram garis untuk kategori casual
sns.lineplot(data=sewa_perjam_df, x='hr', y='casual', ax=axs[0, 0])
axs[0, 0].set_title('Rata-rata Penyewaan Sepeda Casual per Jam')
axs[0, 0].set_xlabel('Jam')
axs[0, 0].set_ylabel('Rata-rata Penyewaan Kasual')

##Membuat diagram garis untuk kategori registered
sns.lineplot(data=sewa_perjam_df, x='hr', y='registered', ax=axs[0, 1])
axs[0, 1].set_title('Rata-rata Penyewaan Sepeda Registered per Jam')
axs[0, 1].set_xlabel('Jam')
axs[0, 1].set_ylabel('Rata-rata Penyewaan Registered')

#Membuat diagram garis untuk total penyewaan
sns.lineplot(data=sewa_perjam_df, x='hr', y='cnt', ax=axs[1, 0])
axs[1, 0].set_title('Rata-rata Total Penyewaan Sepeda per Jam')
axs[1, 0].set_xlabel('Jam')
axs[1, 0].set_ylabel('Rata-rata Penyewaan')

plt.delaxes(axs[1, 1])
plt.tight_layout()
st.pyplot(fig)

st.markdown("""
Pada diagram di atas, dapat dilihat bahwa rata-rata penyewaan sepeda kategori kasual banyak pada jam 12-17 dan memiliki puncak penyewaan jam 14. Pada kategori registered, rata-rata penyewaan ramai pada jam berangkat dan pulang kerja serta memiliki puncak penyewaan pada jam 17. Sedangkan secara total, penyewaan sepeda memiliki puncak rata-rata penyewaan pada jam 17.
""")

st.subheader('Pengaruh temperatur pada penyewaan sepeda')

fig2, ax = plt.subplots(figsize=(16,8))

#Membuat diagram penyewaan sepeda berdasarkan temperatur
temperatur_df[['temp_binned', 'cnt']].plot(x='temp_binned', kind='bar', ax=ax, stacked=False)
ax.set_title('Jumlah Penyewaan Sepeda Berdasarkan Temperatur')
ax.set_xlabel('Temperatur')
ax.set_ylabel('Jumlah Penyewaan')
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(['Rendah (0 - 0.3)', 'Sedang (0.3 - 0.7)', 'Tinggi (0.7 - 1)'], rotation=0)
st.pyplot(fig2)

st.markdown("Sepeda paling banyak disewa pada temperatur tinggi dan paling sedikit disewa pada temperatur rendah.")