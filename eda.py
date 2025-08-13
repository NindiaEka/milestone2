import streamlit as st
import pandas as pd
from PIL import Image
import seaborn as sns
import matplotlib.pyplot as plt

def run_eda():
    st.title("Earthquakes Data Analysis")
    
    gambar = Image.open('ref_gambar/gempabumi.jpg')
    st.image(gambar)

    # Latar belakang
    st.write('# Latar Belakang')
    st.markdown('''
                Menurut laporan [Badan Geologi](https://www.cnbcindonesia.com/news/20250122174037-4-605239/gempa-bumi-merusak-hantam-ri-cetak-rekor-di-2024-fakta-aneh-terungkap), kejadian gempa bumi yang telah mengakibatkan terjadinya korban jiwa, kerusakan bangunan, kerusakan lingkungan dan kerugian harta benda. 
                Kejadian gempa bumi merusak tahun 2024 merupakan yang tertinggi dalam kurun waktu 24 tahun terakhir sejak tahun 2000.
                
                Memprediksi magnitudo gempa bumi menggunakan parameter lokasi, kedalaman, jumlah stasiun seismik, dan indikator akurasi menggunakan data gempa pada tahun 2020 - 2025.  
                
                Tujuannya adalah mendukung BNPB dalam memperkirakan kekuatan gempa lebih cepat sehingga dapat mengoptimalkan penyaluran sumber daya dan evakuasi.
                ''')
    
    # Load dataset langsung
    df = pd.read_csv("data_gempa.csv", sep=",")  # <-- pastikan delimiter sesuai
    
    # tampilkan dataframe rapi
    st.dataframe(df, use_container_width=True)

    st.markdown('''
                Deskripsi dari masing - masing kolom :
                | Kolom            | Deskripsi                                                                 |
                |------------------|---------------------------------------------------------------------------|
                | **time**         | Waktu kejadian gempa dalam format (HH:MM:SS)                              |
                | **latitude**     | Lintang lokasi pusat gempa                                               |
                | **longitude**    | Bujur lokasi pusat gempa                                                 |
                | **depth**        | Kedalaman gempa dalam kilometer (km)                                     |
                | **mag**          | Magnitudo gempa (kekuatan)                                               |
                | **magType**      | Jenis magnitudo, contoh: mb, mww, ml, dll                                |
                | **nst**          | Jumlah stasiun seismik yang digunakan untuk menentukan lokasi gempa      |
                | **gap**          | Sudut gap jaringan seismik (dalam derajat) – semakin kecil semakin baik |
                | **dmin**         | Jarak minimum dari lokasi gempa ke stasiun pengamat (dalam derajat)     |
                | **rms**          | Root Mean Square error dari lokasi gempa (indikator ketidakpastian)     |
                | **net**          | Jaringan (network) yang merekam data gempa                               |
                | **id**           | ID unik untuk kejadian gempa ini                                         |
                | **type**         | Jenis kejadian (umumnya "earthquake")                                     |
                | **horizontalError** | Perkiraan kesalahan horizontal lokasi pusat gempa (dalam km)           |
                | **depthError**   | Perkiraan kesalahan pengukuran kedalaman (dalam km)                      |
                | **magError**     | Perkiraan kesalahan pengukuran magnitudo                                 |
                | **magNst**       | Jumlah stasiun yang digunakan untuk mengukur magnitudo                    |
                | **status**       | Status data (reviewed atau automatic)                                    |
                | **locationSource** | Sumber data lokasi gempa                                                |
                | **magSource**    | Sumber data magnitudo                                                    |
                | **location**     | Keterangan nama kota atau Lokasi gempa tercatat                          |
                | **Date**         | Tanggal kejadian gempa dalam format (YYYY-MM-DD)                         |
                ''')
    
    st.write('# Exploratory Data Analysis')
    # EDA 1 - Tren jumlah gempa
    st.write('## 1. Tren Jumlah Gempa dari Waktu ke Waktu')
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df_count_time = df.groupby(df['date'].dt.to_period('M')).size()
        df_count_time.index = df_count_time.index.to_timestamp()

        plt.style.use('seaborn-v0_8')
        sns.set_palette("coolwarm")

        fig, ax = plt.subplots(figsize=(12, 6))
        df_count_time.plot(kind='line', marker='o', ax=ax)
        plt.title("Tren Jumlah Gempa dari Waktu ke Waktu")
        plt.xlabel("Bulan")
        plt.ylabel("Jumlah Gempa")
        plt.grid(True)
        st.pyplot(fig)
        st.markdown('''
                 Analisis Tren Jumlah Gempa Dari Waktu ke Waktu (2022–2025)

                1. Fluktuasi Signifikan Setiap Tahun
                - Hampir setiap tahun terdapat lonjakan besar jumlah gempa di bulan tertentu.
                - Contoh: awal 2023, pertengahan 2024, dan pertengahan 2025.
                - Lonjakan ini dapat mengindikasikan periode aktivitas seismik lebih tinggi, kemungkinan akibat pergerakan lempeng atau swarm gempa.

                2. Tidak Ada Tren Naik/Turun yang Konsisten
                - Periode 2022–2025 menunjukkan pola naik-turun tajam, tanpa tren meningkat atau menurun yang jelas.
                - Aktivitas gempa bersifat episodik, bukan meningkat secara gradual.

                3. Puncak Ekstrem
                - Puncak tertinggi terjadi sekitar awal–pertengahan 2023 dan pertengahan 2025, dengan jumlah lebih dari 200 kejadian.
                - Puncak semacam ini bisa terkait dengan gempa besar yang memicu serangkaian gempa susulan (aftershocks).

                4. Bulan dengan Aktivitas Rendah
                - Beberapa titik rendah di bawah 50 kejadian, misalnya pertengahan 2024 dan akhir 2025.
                - Titik rendah sering muncul setelah periode aktivitas tinggi, menandakan masa “tenang” sementara.
                ---
                ''')
        
    st.write('## 2. Lokasi Paling Sering Terjadi Gempa')
    # EDA 2 - Top lokasi gempa
    if 'place' in df.columns:
        top_locations = df['place'].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=top_locations.values, y=top_locations.index, ax=ax)
        plt.title("Top 10 Lokasi Paling Sering Terjadi Gempa")
        plt.xlabel("Jumlah Kejadian")
        plt.ylabel("Lokasi")
        st.pyplot(fig)
        st.markdown('''
                 Analisis Top 10 Lokasi Paling Sering Terjadi Gempa

                    1. Pulau-Pulau Tanimbar, Indonesia
                    - Paling sering mengalami gempa dengan **lebih dari 50 kejadian**.
                    - Wilayah ini berada di zona subduksi aktif antara Lempeng Indo-Australia dan Eurasia.

                    2. South of Java, Indonesia
                    - Sekitar **31 kejadian** tercatat.
                    - Termasuk salah satu jalur megathrust selatan Jawa yang rawan gempa besar.

                    3. Kepulauan Babar, Indonesia
                    - Hampir **27 kejadian**.
                    - Terletak dekat pertemuan lempeng yang kompleks, memicu aktivitas seismik tinggi.

                    4. Southwest of Sumatra, Indonesia
                    - Sekitar **26 kejadian**.
                    - Zona ini merupakan bagian dari jalur subduksi Sumatra yang terkenal memicu gempa besar.

                    5–10. Wilayah Lain
                    - **South of Sumbawa** & **Papua**: ±15 kejadian.
                    - **Java**, **near the north coast of Papua**, **Pulau-Pulau Talaud**, dan **Southern Sumatra**: 11–14 kejadian.
                    - Meskipun frekuensinya lebih rendah, beberapa wilayah ini berpotensi mengalami gempa besar akibat posisi di jalur pertemuan lempeng.

                    ---

                    Rekomendasi untuk BNPB
                    1. **Prioritaskan Mitigasi di Top 3 Lokasi**
                    - Tanimbar, selatan Jawa, dan Kepulauan Babar mendapat prioritas dalam edukasi publik dan logistik bencana.
                    2. **Peningkatan Pemantauan Seismik**
                    - Penambahan sensor gempa di wilayah yang memiliki potensi gempa besar.
                    3. **Simulasi & Latihan Evakuasi**
                    - Dilaksanakan secara rutin di wilayah dengan aktivitas seismik tinggi.

                    ---
                ''')
    st.write('## 3. Hubungan Jumlah Stasiun (nst) vs Magnitudo')
    # EDA 3 - Hubungan jumlah stasiun vs magnitudo
    if 'nst' in df.columns and 'mag' in df.columns:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.regplot(x='nst', y='mag', data=df,
                    scatter_kws={'alpha': 0.6},
                    line_kws={'color': 'red'}, ax=ax)
        plt.title('Hubungan Jumlah Stasiun (nst) vs Magnitudo')
        plt.xlabel('Jumlah Stasiun (nst)')
        plt.ylabel('Magnitudo')
        plt.grid(True)
        st.pyplot(fig)
        st.markdown('''
                    **Pola Umum**  
                    - Terdapat hubungan positif: semakin besar magnitudo gempa, semakin banyak stasiun yang mendeteksinya.

                    **Sebaran Data**  
                    - Magnitudo kecil (3,5–4,5): jumlah stasiun relatif sedikit (banyak di bawah 50).
                    - Magnitudo menengah–besar (>5): jumlah stasiun bervariasi, dapat mencapai >300.

                    **Interpretasi**  
                    - Gempa yang lebih besar memiliki gelombang seismik yang lebih kuat dan menjangkau area lebih luas, sehingga terdeteksi oleh lebih banyak stasiun.
                    ---
                    **Implikasi Praktis**  
                    1. Peningkatan jumlah stasiun akan meningkatkan deteksi gempa kecil di wilayah terpencil.  
                    2. Data ini membantu **BNPB/BMKG** memprioritaskan penambahan stasiun di daerah rawan gempa dengan cakupan rendah.  
                    3. Hubungan kuat ini dapat menjadi model awal prediksi magnitudo berdasarkan jumlah stasiun yang menerima sinyal awal.
                    ---
                    ''')
        
    st.write('## 4. Frekuensi Gempa per Kategori Magnitude')
    # EDA 4 - Frekuensi Gempa per Kategori Magnitude
    if 'mag' in df.columns:
        bins = [0, 3, 4, 5, 6, 10]
        labels = ['Micro (<3)', 'Minor (3-3.9)', 'Moderate (4-4.9)', 'Strong (5-5.9)', 'Major (>=6)']
        
        # Membuat kategori magnitudo
        df['mag_category'] = pd.cut(df['mag'], bins=bins, labels=labels, right=False)

        fig, ax = plt.subplots(figsize=(8, 5))
        sns.countplot(y='mag_category', data=df, order=labels, palette='viridis', ax=ax)
        plt.title("Frekuensi Gempa per Kategori Magnitude")
        plt.xlabel("Jumlah kejadian")
        plt.ylabel("Kategori Magnitude")
        st.pyplot(fig)
        st.markdown('''
                     Analisis Frekuensi Gempa per Kategori Magnitudo

                    1. Dominasi Gempa Moderat (4–4.9 SR)
                    - Jumlah kejadian hampir **5.000 gempa**, jauh lebih tinggi dibanding kategori lainnya.
                    - Menunjukkan sebagian besar aktivitas seismik berada pada tingkat sedang yang cukup terasa,
                    namun jarang menimbulkan kerusakan besar jika pusat gempa jauh dari permukiman.

                    2. Gempa Kuat (5–5.9 SR) Relatif Jarang
                    - Hanya sekitar **600-an kejadian**.
                    - Meski jarang, kategori ini berpotensi merusak infrastruktur, terutama jika kedalaman gempa dangkal.

                    3. Gempa Besar (≥6 SR) Sangat Jarang
                    - Jumlahnya sangat sedikit dibanding kategori lain.
                    - Dampak sosial-ekonomi bisa sangat besar walau frekuensinya rendah.

                    4. Gempa Minor & Mikro Hampir Tidak Terdata
                    - Kemungkinan karena keterbatasan sensor atau fokus data pada magnitudo ≥3.
                    - Gempa mikro biasanya terdeteksi di jaringan seismograf lokal dan jarang dilaporkan jika tidak signifikan.

                    ---

                    Rekomendasi untuk BNPB
                    1. **Edukasi Publik Tentang Gempa Moderat**
                    - Mengajarkan langkah mitigasi sederhana saat guncangan terasa.
                    2. **Penguatan Infrastruktur Kritis**
                    - Standarisasi bangunan tahan gempa minimal untuk magnitudo 5 SR.
                    3. **Peningkatan Sistem Peringatan Dini Lokal**
                    - Memperbanyak sensor di wilayah rawan untuk memantau gempa kecil–sedang.
                    ---
                    ''')

    st.write('## 5. Hubungan Kedalaman dan Magnitude Gempa')
    # EDA 5 - Hubungan Kedalaman dan Magnitude
    if 'depth' in df.columns and 'mag' in df.columns:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.regplot(
            x='depth', 
            y='mag', 
            data=df,
            scatter_kws={'alpha': 0.7},       
            line_kws={'color': 'red', 'linewidth': 2}, 
            ax=ax
        )
        plt.title("Hubungan Kedalaman dan Magnitude Gempa")
        plt.xlabel("Kedalaman (km)")
        plt.ylabel("Magnitude")
        plt.grid(True)
        st.pyplot(fig)
        st.markdown('''
                     Analisis Hubungan Kedalaman dan Magnitude Gempa
                        Pola Hubungan
                        - Garis tren regresi menunjukkan hubungan yang **cenderung datar**.
                        - Perubahan kedalaman **tidak secara signifikan** memengaruhi besarnya magnitudo gempa.

                        Sebaran Data
                        - Magnitudo gempa umumnya berada di kisaran **4,0–5,5**.
                        - Beberapa gempa besar (di atas 6,0) terjadi di berbagai kedalaman, baik dangkal maupun menengah.
                        - Sebaran titik relatif merata pada kedalaman 0–100 km, tanpa pola peningkatan atau penurunan yang jelas.
                    
                    ''')
