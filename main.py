import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np 


st.set_page_config(
    page_title="Rekomendasi Destinasi Pariwisata Indonesia: 5 Kota untuk Dikunjungi",
    page_icon="🏞️",
    layout="centered"
)

with st.sidebar:
    st.title('**Panelist - Dashboard Review**')
    st.markdown(
        """
            **Let's connect on linkedin**
            https://www.linkedin.com/in/salma-eka-y/
        **sumber data:**
        1. mediakeuangan.kemenkeu.go.id
        > Kian Melesat di 2023, Pariwisata Indonesia Bersiap Menuju Level Prapandemi
        2. bps
        > Jumlah Perjalanan Wisatawan Nasional (Perjalanan), 
        Jumlah Kunjungan Wisatawan Mancanegara per bulan ke Indonesia Menurut Pintu Masuk 
        3. Kaggle
        > Indonesia Tourism Destination 
            
           
        """

    )


st.header("Rekomendasi Destinasi Pariwisata Indonesia: 5 Kota untuk Dikunjungi")
"by Salma Eka Yudanti (salmaey2022@gmail.com)"
st.markdown('<br>', unsafe_allow_html=True)

st.markdown('''<div style="text-align:justify;font-size:18px;">
            Indonesia memiliki banyak potensi pariwisata. Hal ini terbukti dari bagaimana industri pariwisata Indonesia
            tumbuh dan berkembang dengan sangat cepat. Pada kenyataannya, berbagai prestasi Indonesia yang telah mendapat 
            pengakuan internasional menjadi pengingat akan pertumbuhan industri pariwisata yang sangat pesat.</div>
            ''', unsafe_allow_html=True)

st.markdown('\n')
 
st.markdown('<div style="text-align:justify;font-size:18px;">Salah satu penopang ekonomi Indonesia dan sumber devisa yang \
            signifikan adalah industri pariwisata. Menurut Kebijakan Pariwisata 2022 dari Organisasi \
                Kerja Sama Ekonomi dan Pembangunan (OECD), <font color= cyan>industri pariwisata menyumbang 5,0%</font> dari PDB Indonesia \
                        pada tahun 2019. </div>', unsafe_allow_html=True)
st.markdown('<br>', unsafe_allow_html=True)

image = Image.open('o_1b69p1552art15981haoujc1hs9a.jpg')
st.image(image, caption='scr: google.com')


df_jumlahwisatawan = pd.read_csv('jumlah_wisatawan.csv')
df_wisatawan = pd.read_csv('nasionaldanmanca.csv')

st.markdown('''<div style="text-align:justify;font-size:18px;">
            Jumlah pengunjung Nusantara dan Mancanegara 
            telah meningkat dari tahun ke tahun. Jumlah pengunjung Nusantara meningkat dari 257.818 pada bulan Mei 
            2022 menjadi 592.855 pada bulan Mei 2023. Sementara itu, jumlah pengunjung Mancanegara meningkat dari 354.920 
            pada bulan Mei 2022 menjadi 953.713 pada bulan Mei 2023.
            </div>
            ''', unsafe_allow_html=True)

st.markdown('<br>', unsafe_allow_html=True)

df_jumlahwisatawan['Tanggal'] = pd.to_datetime(df_jumlahwisatawan['Tanggal'])
# Multiselect untuk memilih kategori
multitahun = st.multiselect(
    "Pilih Kategori Wisatawan",
    ['Nusantara', 'Mancanegara'],
    default=['Nusantara']
)
st.markdown('<br>', unsafe_allow_html=True)

# Filter data berdasarkan kategori yang dipilih
filtered_df = df_wisatawan[df_wisatawan['Kategori'].isin(multitahun)]

# Membuat chart line dengan titik dan label hover
chart = alt.Chart(filtered_df).encode(
    x=alt.X('Tanggal:T', title='Bulan'),
    y=alt.Y('Jumlah:Q', title='Jumlah', aggregate='sum'),
    color='Kategori:N',
)

# Menambahkan garis
line = chart.mark_line()
line = line.properties(
    title=f"Jumlah Wisatawan pada Kategori {', '.join(map(str, multitahun))}"
)

# Menambahkan titik dengan label hover
circle = chart.mark_circle(size=60).encode(
    tooltip=['Tanggal:T', 'Jumlah:Q', 'Kategori:N']
)

# Gabungkan garis dan titik
combined_chart = (line + circle)

st.altair_chart(combined_chart, use_container_width=True)

# filter ScatterPlot to City
df_turisWithId = pd.read_csv('tourism_with_id.csv')

st.markdown('\n')


@st.cache_resource
def load_data():
    df = pd.read_csv('tourism_with_id.csv')
    return df


df = load_data()

category_counts1 = df_turisWithId['City'].value_counts().reset_index()
category_counts1.columns = ['City', 'Count']

# Buat plot batang
st.markdown('<div style="text-align:justify;font-size:30px;">Jumlah Destinasi di Setiap Kota</div>',unsafe_allow_html=True)
lap = px.bar(category_counts1, x="City", y="Count",
             color="City")
lap.update_layout(
    autosize=False,
    width=800,
    height=500
)

st.plotly_chart(lap, use_container_width=True)

with st.expander('**Penjelasan Visualisasi:**'):
    st.markdown('''
               Bar chart tersebut menunjukkan jumlah destinasi di masing-masing Kota.\
               Kota Yogyakarta memiliki 126 destinasi pariwisata, Bandung 124, Jakarta 84, Semarang 57, dan Surabaya 46
               ''')

st.markdown('\n')

st.markdown('<div style="text-align:justify;font-size:30px;">Sebaran Harga Destinasi di Setiap Kota</div>',unsafe_allow_html=True)

# Multi-select untuk Kota
selected_cities = st.multiselect(
    "Pilih Kota", df['City'].unique(), default=df['City'].unique())

filtered_df = df[df['City'].isin(selected_cities)]

# Membuat plot
fig = px.box(filtered_df, x="City", y="Price",
             title="Sebaran Data", hover_data=['Place_Name'], color="City")
st.plotly_chart(fig)

with st.expander('**Penjelasan Visualisasi:**'):
    st.markdown('''
                Visualisasi di atas menggambarkan perbandingan harga destinasi berdasarkan kategori kota. Kelima kota tersebut 
                masing-masing memiliki harga terendah yaitu 0K. Harga tertinggi di kota Jakarta dengan
                harga 900K, Yogjakarta 500k, Bandung 375k, Semarang 200k, dan Surabaya 125k. 
                \nFaktor yang menyebabkan 
                jakarta terlihat mahal
                dari kota yang lainnya adalah disebabkan oleh kota metropolitan yang memiliki biaya hidup yang tinggi,
                memiliki banyak tempat wisata yang populer, 
                sehingga biaya masuknya pun relatif tinggi. Bandung, Yogjakarta, dan Semarang memiliki banyak tempat 
                wisata yang menarik, sehingga biaya masuknya pun relatif tinggi. Sedangkan Surabaya memiliki sedikit destinasi pariwisata.
                ''')



# ScatterPlot
# st.header("""
#          Persebaran Rating dan Harga menurut Kota
#          """
#           )
# selected_cities = st.multiselect(
#     "Pilih Kota", df['City'].unique(), default=df['City'].unique())

# # Filter data based on selected cities
# filtered_dfKota = df[df['City'].isin(selected_cities)]

# # Create a scatter plot
# filtered_dfKota['Symbol'] = pd.Categorical(filtered_dfKota['Place_Name']).codes

# scatter = px.scatter(filtered_dfKota, x='Rating', y='Price',
#                      color='City', hover_data=['Place_Name'], title="Scatter Plot")

# st.plotly_chart(scatter, use_container_width=True)

# st.markdown('<div style="text-align:justify;font-size:18px;">Scatterplot tersebut menunjukkan hubungan antara harga dan rating dari lima kota di Indonesia,\
#         yaitu Jakarta, Bandung, Yogyakarta, Semarang, dan Surabaya. Scatterplot ini menunjukkan hubungan negatif antara harga dan rating, yang berarti bahwa semakin tinggi rating, semakin rendah harga. Scatterplot juga menunjukkan bahwa Yogyakarta memiliki rating tertinggi dan harga terendah.</div>',
#             unsafe_allow_html=True)

# Bar Chart
category_counts = df_turisWithId['Category'].value_counts().reset_index()
category_counts.columns = ['Category', 'Count']

# Buat plot batang
st.header('Jumlah Kategori Destinasi di 5 Kota')
lap = px.bar(category_counts, x="Category", y="Count",
             color="Category")
lap.update_layout(
    autosize=False,
    width=800,
    height=500
)

st.plotly_chart(lap, use_container_width=True)

with st.expander('Penjalasan Visualisasi'):
    st.markdown('Bar chart tersebut menunjukkan jumlah kategori destinasi yang berbeda.\
    Kategori-kategori tersebut adalah “Taman Hiburan”, “Budaya”, Bahari, “Cagar Alam”, “Tempat Ibadah”, dan “Pusat Perbelanjaan”.\
        Jumlah tertinggi adalah “Taman Hiburan” diangka 135, dan jumlah terendah adalah “Pusat Perbelanjaan” diangka 15.')


# Tampilkan radio button untuk pemilihan kota
selected_city = st.radio('Select City', df['City'].unique())

# Filter data berdasarkan kota yang dipilih
filtered_data = df[df['City'] == selected_city]
st.header(f'Jumlah Kategori Destinasi di {selected_city}')

# Hitung jumlah kategori di setiap kota
category_counts = filtered_data['Category'].value_counts().reset_index()
category_counts.columns = ['Category', 'Count']

# Buat plot batang
fig = px.bar(category_counts, x="Category", y="Count", color="Category")
fig.update_layout(
    autosize=False,
    width=800,
    height=500
)

# Tampilkan plot batang yang dapat di-filter
st.plotly_chart(fig, use_container_width=True)

with st.expander('Penjalasan Visualisasi'):
    st.markdown('''Jika dilihat, Kota Jakarta memiliki destinasi Budaya terbanyak, Yogyakarta yaitu taman hiburan, 
                Bandung dan Semarang yaitu cagar alam, dan Surabaya yaitu taman hiburan''')


# st.markdown('<div style="text-align:justify;font-size:18px;">Indonesia memiliki banyak kota yang memiliki potensi wisata menarik.\
#     Namun, jika mencari rekomendasi kota-kota terbaik untuk dikunjungi, maka Destinasi Pariwisata Indonesia: 5 Kota untuk \
#         Dikunjungi mungkin bisa menjadi referensi. Lima kota terbaik di Indonesia yang menawarkan berbagai tempat wisata menarik, \
#             yaitu <font color=orange>Jakarta, Bandung, Yogyakarta, Semarang, dan Surabaya</font>. Setiap kota memiliki daya tariknya sendiri-sendiri, mulai\
#                 dari keindahan alam hingga kekayaan budaya. Misalnya, Yogyakarta memiliki sejarah dan tradisi yang kaya, sedangkan\
#                     Bandung menawarkan berbagai tempat wisata menarik seperti Gunung Tangkuban Perahu dan Kawah Putih. Jakarta sendiri\
#                         memiliki banyak tempat wisata menarik seperti Monumen Nasional (Monas) dan Taman Mini Indonesia Indah. \
#                             Semua kota tersebut dapat menjadi pilihan yang tepat untuk liburan selanjutnya.</div>',
#             unsafe_allow_html=True)

st.header('Saran')
st.markdown('''<div style="text-align:justify;font-size:18px;">
            Berdasarkan informasi mengenai jumlah destinasi pariwisata, harga, kategori destinasi, dan faktor-faktor lain yang memengaruhi harga, berikut adalah saran untuk rekomendasi destinasi pariwisata yang bisa dikunjungi:
\nYogyakarta:

\nKunjungi taman hiburan yang jumlahnya tertinggi di Yogyakarta dengan harga relatif terjangkau sebesar 500K. Jelajahi juga destinasi budaya yang ada di kota ini.
\n
\nBandung:

Bandung memiliki beragam destinasi cagar alam dan taman hiburan dengan harga yang cukup bersaing. Disarankan untuk menjelajahi cagar alam dan menikmati hiburan yang ditawarkan kota ini.

\nJakarta:

Meskipun Jakarta memiliki harga masuk tertinggi, destinasi budaya di kota ini patut untuk dikunjungi. Pilih destinasi yang sesuai minat dan nikmati pengalaman unik di ibukota.
Semarang:

\nSemarang:
\nTerdapat banyak destinasi cagar alam di Semarang dengan harga yang cukup terjangkau. Jelajahi keindahan alam dan nikmati budaya lokal yang khas.

\nSurabaya:

Meski Surabaya memiliki sedikit destinasi pariwisata, Anda dapat mengeksplor taman hiburan yang tersedia dengan harga masuk yang lebih terjangkau. Selain itu, nikmati atmosfer kota yang kaya sejarah.
            ''', unsafe_allow_html=True)



# # FILTER
# # Membaca data dari file 'tourism_with_id.csv'
# data = pd.read_csv('tourism_with_id.csv')

# # Filter City (Kota) dan Category (Kategori) menjadi 2 kolom
# st.header('Filter')
# col1, col2 = st.columns(2)

# with col1:
#     city = st.radio("Pilih Kota (City)", data['City'].unique())

# with col2:
#     category = st.radio("Pilih Kategori (Category)", data['Category'].unique())

# # Tombol untuk menampilkan rekomendasi
# if st.button("Tampilkan Filter"):
#     # Filter data berdasarkan kriteria yang dipilih
#     filtered_data = data[
#         (data['City'] == city) &
#         (data['Category'] == category)
#     ]

#     # Menampilkan tabel rekomendasi
#     if not filtered_data.empty:
#         st.header('Tabel Rekomendasi')
#         st.dataframe(filtered_data[['City', 'Category',
#                                     'Place_Name', 'Description', 'Price', 'Rating']])
#     else:
#         st.info('Tidak ada rekomendasi yang sesuai dengan kriteria yang dipilih.')

# st.markdown('<div style="text-align:justify;font-size:18px;">Dengan filter tersebut, kita dapat membandingkan jumlah Kota yang berbeda dengan membandingkan jumlah kategori destinasi yang berbeda yang tersedia di tempat lain.</div>',
#             unsafe_allow_html=True)
