import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px
import altair as alt

st.set_page_config(
    page_title="Destinasi Pariwisata Indonesia: 5 Kota untuk Dikunjungi",
    page_icon="🏞️",
    layout="centered"
)

with st.sidebar:
    st.title('**Panelist - Dashboard Review**')
    st.subheader('This is the basis for one of the recruitment processes')
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


st.header("Destinasi Pariwisata Indonesia: 5 Kota untuk Dikunjungi")
"by Salma Eka Yudanti (salmaey2022@gmail.com)"
st.markdown('<br>', unsafe_allow_html=True)

st.markdown('<div style="text-align:justify;font-size:18px;">Salah satu penopang ekonomi Indonesia dan sumber devisa yang \
            signifikan adalah industri pariwisata. Menurut Kebijakan Pariwisata 2022 dari Organisasi \
                Kerja Sama Ekonomi dan Pembangunan (OECD), <font color= cyan>industri pariwisata menyumbang 5,0%</font> dari PDB Indonesia \
                        pada tahun 2019. <font color = red>Namun, dampak pandemi COVID-19</font> menyebabkan penurunan kontribusi PDB \
                            pariwisata sebesar <font color= cyan>56%</font> menjadi hanya <font color= red>2,2% dari keseluruhan ekonomi di tahun 2020.\
                                </div>', unsafe_allow_html=True)
st.markdown('<br>', unsafe_allow_html=True)

image = Image.open('o_1b69p1552art15981haoujc1hs9a.jpg')
st.image(image, caption='scr: google.com')


df_jumlahwisatawan = pd.read_csv('jumlah_wisatawan.csv')
df_wisatawan = pd.read_csv('nasionaldanmanca.csv')

st.markdown('<div style="text-align:justify;font-size:18px;">Berbagai upaya untuk membangkitkan sektor pariwisata yang mati suri selama pandemi berbuah manis.\
            Pada 2022, jumlah kunjungan wisatawan mancanegara(wisman) maupun wisatawan nusantara(wisnus) berhasil melampaui target. </div >',
            unsafe_allow_html=True)
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

st.markdown('<div style="text-align:justify;font-size:18px;">Indonesia memiliki banyak kota yang memiliki potensi wisata menarik.\
    Namun, jika mencari rekomendasi kota-kota terbaik untuk dikunjungi, maka Destinasi Pariwisata Indonesia: 5 Kota untuk \
        Dikunjungi mungkin bisa menjadi referensi. Lima kota terbaik di Indonesia yang menawarkan berbagai tempat wisata menarik, \
            yaitu <font color=orange>Jakarta, Bandung, Yogyakarta, Semarang, dan Surabaya</font>. Setiap kota memiliki daya tariknya sendiri-sendiri, mulai\
                dari keindahan alam hingga kekayaan budaya. Misalnya, Yogyakarta memiliki sejarah dan tradisi yang kaya, sedangkan\
                    Bandung menawarkan berbagai tempat wisata menarik seperti Gunung Tangkuban Perahu dan Kawah Putih. Jakarta sendiri\
                        memiliki banyak tempat wisata menarik seperti Monumen Nasional (Monas) dan Taman Mini Indonesia Indah. \
                            Semua kota tersebut dapat menjadi pilihan yang tepat untuk liburan selanjutnya.</div>',
            unsafe_allow_html=True)


@st.cache_resource
def load_data():
    df = pd.read_csv('tourism_with_id.csv')
    return df


df = load_data()

# ScatterPlot
st.header("""
         Persebaran Rating dan Harga menurut Kota
         """
          )
selected_cities = st.multiselect(
    "Pilih Kota", df['City'].unique(), default=df['City'].unique())

# Filter data based on selected cities
filtered_dfKota = df[df['City'].isin(selected_cities)]

# Create a scatter plot
filtered_dfKota['Symbol'] = pd.Categorical(filtered_dfKota['Place_Name']).codes

scatter = px.scatter(filtered_dfKota, x='Rating', y='Price',
                     color='City', hover_data=['Place_Name'], title="Scatter Plot")

st.plotly_chart(scatter, use_container_width=True)

st.markdown('<div style="text-align:justify;font-size:18px;">Scatterplot tersebut menunjukkan hubungan antara harga dan rating dari lima kota di Indonesia,\
        yaitu Jakarta, Bandung, Yogyakarta, Semarang, dan Surabaya. Scatterplot ini menunjukkan hubungan negatif antara harga dan rating, yang berarti bahwa semakin tinggi rating, semakin rendah harga. Scatterplot juga menunjukkan bahwa Yogyakarta memiliki rating tertinggi dan harga terendah.</div>',
            unsafe_allow_html=True)

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

st.markdown('<div style="text-align:justify;font-size:18px;">Bar chart tersebut menunjukkan jumlah kategori destinasi yang berbeda.\
    Kategori-kategori tersebut adalah “Taman Hiburan”, “Budaya”, Bahari, “Cagar Alam”, “Tempat Ibadah”, dan “Pusat Perbelanjaan”.\
        Jumlah tertinggi adalah “Taman Hiburan” diangka 135, dan jumlah terendah adalah “Pusat Perbelanjaan” diangka 15.</div>',
            unsafe_allow_html=True)

# FILTER
# Membaca data dari file 'tourism_with_id.csv'
data = pd.read_csv('tourism_with_id.csv')

# Filter City (Kota) dan Category (Kategori) menjadi 2 kolom
st.header('Filter')
col1, col2 = st.columns(2)

with col1:
    city = st.radio("Pilih Kota (City)", data['City'].unique())

with col2:
    category = st.radio("Pilih Kategori (Category)", data['Category'].unique())

# Tombol untuk menampilkan rekomendasi
if st.button("Tampilkan Filter"):
    # Filter data berdasarkan kriteria yang dipilih
    filtered_data = data[
        (data['City'] == city) &
        (data['Category'] == category)
    ]

    # Menampilkan tabel rekomendasi
    if not filtered_data.empty:
        st.header('Tabel Rekomendasi')
        st.dataframe(filtered_data[['City', 'Category',
                                    'Place_Name', 'Description', 'Price', 'Rating']])
    else:
        st.info('Tidak ada rekomendasi yang sesuai dengan kriteria yang dipilih.')

st.markdown('<div style="text-align:justify;font-size:18px;">Dengan filter tersebut, kita dapat membandingkan jumlah Kota yang berbeda dengan membandingkan jumlah kategori destinasi yang berbeda yang tersedia di tempat lain.</div>',
            unsafe_allow_html=True)
