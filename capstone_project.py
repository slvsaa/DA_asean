# Import Library
import streamlit as st
import pandas as pd
import numpy as np
import hydralit_components as hc
import plotly.express as px
import plotly.graph_objects as go
from numerize import numerize

st.set_page_config(page_title="Pendidikan di ASEAN", page_icon = "🎓", layout = 'wide', initial_sidebar_state = 'auto')

# Warna Backgound
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-color:#E7E0C9
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Metric wo/ Arrow
st.write(
    """
    <style>
    [data-testid="stMetricDelta"] svg {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Navbar
menu_data = [
        {'icon': "bi bi-geo-alt", 'label':"by Country", 'ttip':"Dashboard Based on Country"},
        {'icon': "bi bi-app-indicator", 'label':"by Indicator", 'ttip':"Dashboard Based on Indicator"},
        {'icon': "far fa-address-book", 'label':"Info", 'ttip':"Contact"}
]

over_theme = {'txc_inactive': 'white','menu_background':'#6B7AA1','txc_active':'#11324D','option_active':'#E7E0C9'}
menu_id = hc.nav_bar(menu_definition=menu_data, home_name='Home', override_theme=over_theme)

# Import Dataset
df_main = pd.read_csv('df_merge.csv')
df_main["Year"] = df_main["Year"].astype("str")
df_main.drop(['Unnamed: 0'], axis=1, inplace=True)
list_main = [df_main]

# Format penulisan
p_format = '<p style="color:Black; font-size: 16px; text-align: justify">'

# Halaman Home
if menu_id == 'Home':
    st.title('Pendidikan di ASEAN')
    st.text("oleh Silvia Atika Anggrayni")
    st.markdown("---")

    st.markdown(p_format+
                '<b>Pada awal tahun 2023, World Population Review mempublikasikan Rata-Rata IQ berdasarkan Negara pada lamannya. </b>'\
                'IQ atau Intelligence Quotient merupakan salah satu tolak ukur untuk menilai kecerdasan seseorang dengan cara '\
                'mengikuti tes, semakin tinggi angkanya maka semakin tinggi pula kecerdasan orang tersebut. '\
                'Indoensia sendiri mendapat peringkat 130 dari seluruh negara dengan Rata-Rata IQ 78,49. ', unsafe_allow_html=True)
    st.subheader('Bagaimana peringkat Indonesia di antara negara-negara ASEAN?')

    col1,col2 = st.columns([1,1])
    with col1:
        st.markdown(p_format+
                'Peringkat IQ negara ASEAN dapat dilihat di <b>Diagram Rata-Rata IQ di ASEAN</b>. Diagram tersebut telah dirurutkan berdasarkan peringkatnya. '\
                'Dapat dilihat bahwa Indonesia berada diperingkat 2 terakhir, dengan Singapura berada diperingkat teratas dan Timor Leste berada diperingkat terakhir. '\
                'Timor Leste berada diperingkat terakhir namun IQ yang dimiliki sama dengan Indonesia.' ,unsafe_allow_html=True)
        
        st.markdown(p_format+
                '<b>Dilansir dari World Population Review</b>, Skor IQ dapat mencerminkan kualitas pendidikan dan sumber daya yang dimiliki seseorang. '\
                'Maka dengan melihat Rata-Rata IQ di suatu negara, kita juga dapat menilai kualitas pendidikan di negara tersebut. '\
                'Wilayah dengan skor IQ rendah biasanya lebih miskin dan kurang berkembang, khususnya di bidang pendidikan, '\
                'dibandingkan dengan negara yang memiliki skor IQ yang tinggi. ',unsafe_allow_html=True)
        st.markdown(p_format+
                'Dengan adanya pernyataan tersebut, <b>apakah kualitas pendidikan Indonesia termasuk buruk dibanding dengan negara ASEAN lainnya? </b>'\
                'Analisis berikut akan melihat bagaimana setiap negara ASEAN mengalokasikan PDB (Produk Domestik Bruto) untuk pendidikan '\
                'dan seberapa besar masyarakat yang tidak mendapat pendidikan',unsafe_allow_html=True)
    with col2:
        # Data Negara dan IQ
        df_rank = df_main[['Rank IQ','Nama Negara','IQ']].drop_duplicates().sort_values('Rank IQ')

        # Bar Chart
        default_color = "#C1CFC0"
        colors = {"Indonesia": "#A459D1"}

        color_discrete_map = {
            c: colors.get(c, default_color) 
            for c in df_rank['Nama Negara'].unique()}

        rank_chart = px.scatter(df_rank, x='IQ', y='Nama Negara', color='Nama Negara',
                    color_discrete_map=color_discrete_map, size='IQ', hover_name="Nama Negara", hover_data=["IQ", "Rank IQ"])
        rank_chart.update_traces(showlegend=False)
        rank_chart.update_layout(title_text='Rata-Rata IQ di ASEAN', title_x=0.4)

        # Rata-Rata
        rank_chart.add_vline(x=np.nanmean(df_rank['IQ']), line_color="red")
        rank_chart.add_annotation(text='AVG '+ str(round(np.nanmean(df_rank['IQ']),2)),
                  x=np.nanmean(df_rank['IQ'])+2.5, y=1, showarrow=False)
        rank_chart.update_annotations(font=dict(size=14, color="red"))

        # Show Chart
        st.plotly_chart(rank_chart, use_container_width=True)

    # PDB dan Pengeluaran Pendidikan    
    st.subheader('PDB dan Pengeluaran untuk Pendidikan Setiap Negara')
    df_combo2 = df_main[['Rank IQ','Nama Negara', 'PDB dalam USD','Total pengeluaran pemerintah untuk pendidikan',
                         'Total Populasi','Pengeluaran pemerintah untuk pendidikan, total (% dari PDB)']].sort_values('Rank IQ')
    df_combo2 = df_combo2.groupby(['Rank IQ','Nama Negara'])[['PDB dalam USD','Total pengeluaran pemerintah untuk pendidikan',
                         'Total Populasi','Pengeluaran pemerintah untuk pendidikan, total (% dari PDB)']].mean().reset_index()

    fig12 = go.Figure(data=[
        go.Bar(name='PDB dalam USD', 
               x=df_combo2['Nama Negara'], 
                y=df_combo2['PDB dalam USD'],
                text=df_combo2['PDB dalam USD']),
        go.Bar(name='Pengeluaran Pendidikan', 
                x=df_combo2['Nama Negara'], 
                y=df_combo2['Total pengeluaran pemerintah untuk pendidikan'],
                text=df_combo2['Total pengeluaran pemerintah untuk pendidikan'],
                hovertext=round(df_combo2['Pengeluaran pemerintah untuk pendidikan, total (% dari PDB)'],2),
                hovertemplate ='%{hovertext}%'
        ),
    ])
    fig12.add_trace(
            go.Scatter(
                x=df_combo2['Nama Negara'],
                y=df_combo2['Total Populasi'],
                yaxis="y2",
                name="Total Populasi",
                hovertext=round(df_combo2['Total Populasi'],2)
        )
    )

    fig12.update_layout(
        title_text='Perbandingan Rata-Rata PDB dan Pengeluaran Pendidikan tiap Negara (2017-2021)', 
        title_x=0.2,
            legend=dict(
                orientation="h",
                y=-0.1,
                x=0
        ),
        yaxis=dict(
            title=dict(text="Uang dalam USD"),
            side="left",
        ),
        yaxis2=dict(
            title=dict(text="Populasi"),
            side="right",
            overlaying="y",
            tickmode="sync",
    ))
    fig12.update_traces(texttemplate='%{text:.3s}')

    column1, column2, column3, column4 = st.columns([1,1,1,1])
    with col1:
        # AVG PBD
        avg_pdb = numerize.numerize(float(df_combo2['PDB dalam USD'].mean()))
        column1.metric("Rata-Rata PDB dalam USD", avg_pdb)

        # AVG Pendidikan
        avg_pendidikan = numerize.numerize(float(df_combo2['Total pengeluaran pemerintah untuk pendidikan'].mean()))
        column2.metric("Rata-Rata Pengeluaran Pendidikan", avg_pendidikan, '-')

        # AVG Presentase pendidikan
        avg_presentase_pendidikan = round(df_combo2['Pengeluaran pemerintah untuk pendidikan, total (% dari PDB)'].mean(),2)
        column2.metric("Rata-Rata Pengeluaran Pendidikan (% dari PDB)", avg_presentase_pendidikan)

        # Max Pendidikan
        max_pendidikan = df_combo2[['Nama Negara', 'Total pengeluaran pemerintah untuk pendidikan']].sort_values('Total pengeluaran pemerintah untuk pendidikan')[-1:]
        negara_max_pendidikan = max_pendidikan.iloc[0]['Nama Negara']
        value_max_pendidikan = numerize.numerize(float(max_pendidikan.iloc[0]['Total pengeluaran pemerintah untuk pendidikan']))
        column3.metric("Pengeluaran Pendidikan Tertinggi", negara_max_pendidikan, value_max_pendidikan)

        # Max Presentase
        max_presentase = df_combo2[['Nama Negara', 'Pengeluaran pemerintah untuk pendidikan, total (% dari PDB)']].sort_values('Pengeluaran pemerintah untuk pendidikan, total (% dari PDB)')[-1:]
        negara_max_presentase = max_presentase.iloc[0]['Nama Negara']
        value_max_presentase = round(max_presentase.iloc[0]['Pengeluaran pemerintah untuk pendidikan, total (% dari PDB)'],2)
        column3.metric("Pengeluaran Pendidikan Tertinggi (% dari PDB)", negara_max_presentase, value_max_presentase)

        # MIN Pendidikan
        min_pendidikan = df_combo2[['Nama Negara', 'Total pengeluaran pemerintah untuk pendidikan']].sort_values('Total pengeluaran pemerintah untuk pendidikan')[:1]
        negara_min_pendidikan = min_pendidikan.iloc[0]['Nama Negara']
        value_min_pendidikan = numerize.numerize(float(min_pendidikan.iloc[0]['Total pengeluaran pemerintah untuk pendidikan']))
        column4.metric("Pengeluaran Pendidikan Terendah", negara_min_pendidikan, value_min_pendidikan, delta_color="inverse")

        # MIN Pendidikan
        min_presentase = df_combo2[['Nama Negara', 'Pengeluaran pemerintah untuk pendidikan, total (% dari PDB)']].sort_values('Pengeluaran pemerintah untuk pendidikan, total (% dari PDB)')[:1]
        negara_min_presentase = min_presentase.iloc[0]['Nama Negara']
        value_min_presentase = round(min_presentase.iloc[0]['Pengeluaran pemerintah untuk pendidikan, total (% dari PDB)'],2)
        column4.metric("Pengeluaran Pendidikan Terendah (% dari PDB)", negara_min_presentase, value_min_presentase, delta_color="inverse")

    
    # Change the bar mode
    fig12.update_layout(barmode='group')
    st.plotly_chart(fig12, use_container_width=True)
    st.caption('Giga (simbol G) adalah sebuah awalan satuan dalam sistem metrik yang menunjukkan faktor miliar (1.000.000.000).')

    st.markdown(p_format+
                'Dilihat dari nominal, pengeluaran pemerintah Indonesia untuk pendidikan lebih besar dibanding negara lainnya dan Timor Leste memiliki pengeluaran terendah. '\
                'Namun secara presentase, pengeluaran pendidikan Timor Leste paling tinggi dibanding negara lain, hal ini tentu wajar melihat PDB yang dimiliki Timor Leste.'\
                'Secara rata-rata pengeluaran, ada 2 Negara dengan IQ diatas rata-rata yang memiliki pengeluaran pendidikan dibawah rata-rata yaitu Kamboja dan Myanmar,'\
                'sedangkan negara dengan IQ di bawah rata-rata ada 3 negara yaitu Brunei, Laos, dan Timor Leste.', unsafe_allow_html=True)
    st.markdown(p_format+
                'Jika melihat dari presentasenya, Singapura, Kamboja, Myanmar, Thailand, dan Laos memiliki presentase terendah. '\
                'Padahal 4 dari 5 negara tersebut merupakan neagar yang memiliki IQ diatas rata-rata IQ ASEAN.', unsafe_allow_html=True)
    
    # Pemuda
    st.subheader('Populasi Pemuda yang tidak sekolah, kerja, maupun pelatihan')
    # Data chart 2
    df_combo = df_main[['Rank IQ','Nama Negara', 'Total of youth not in education, employment or training', 
                            'Total pengeluaran pemerintah untuk pendidikan','Total Youth',
                            'Share of youth not in education, employment or training, total (% of youth population)']].sort_values('Rank IQ')
    
    df_combo = df_combo.groupby(['Rank IQ','Nama Negara'])[['Total of youth not in education, employment or training', 
                            'Total pengeluaran pemerintah untuk pendidikan','Total Youth',
                            'Share of youth not in education, employment or training, total (% of youth population)']].mean().reset_index()

    col5,col6 = st.columns([1,1])
    with col5:
        st.markdown(p_format+
                'Diagram disamping menunjukkan perbandingan total pemuda seluruhnya dengan total pemuda yang tidak sekolah, kerja, maupun mengikuti pelatihan '\
                'Jika dilihat dari diagram, jumlah pemuda tidak bersekolah paling banyak berada di Indonesia. Namun, jika memerhatikan besarnya '\
                'presentase setiap negara, Timor Leste memiliki 31% Pemuda tidak sekolah dari total pemuda yang berada di Timor Leste', unsafe_allow_html=True)

        st.markdown(p_format+
                'Jika dilihat lebih detail lagi, negara yang memiliki IQ yang melebihi Rata-Rata IQ di ASEAN memiliki presentase kurang dari 20%'\
                'pemuda tidak bersekolah, sedangkan yang berada dibawah rata-rata mencapai 15-30% ', unsafe_allow_html=True)    
    with col6:
        # avg_tdk_sekolah = round(df_combo['Share of youth not in education, employment or training, total (% of youth population)'].mean(),2)
        # col6.metric("Rata-Rata Pemuda Tidak Bersekolah (% of populasi pemuda)", avg_tdk_sekolah)

        fig11 = go.Figure(
            data=go.Bar(
                x=df_combo['Nama Negara'],
                y=df_combo['Total pengeluaran pemerintah untuk pendidikan'],
                name="Pengeluaran Pendidikan",
                text=df_combo['Total pengeluaran pemerintah untuk pendidikan']
            )
        )

        fig11.add_trace(
            go.Scatter(
                x=df_combo['Nama Negara'],
                y=df_combo['Total of youth not in education, employment or training'],
                yaxis="y2",
                name="Pemuda Tidak sekolah",
                hovertext=round(df_combo['Share of youth not in education, employment or training, total (% of youth population)'],2),
                hovertemplate ='%{hovertext}%'
            )
        )

        fig11.add_trace(
            go.Scatter(
                x=df_combo['Nama Negara'],
                y=df_combo['Total Youth'],
                yaxis="y2",
                name="Total pemuda",
                # marker=dict(color="crimson"),
            )
        )

        fig11.update_layout(
            title_text='Rata-Rata Pengeluaran dan Total Pemuda yang Tidak Bersekolah (2017-2021)', 
                        title_x=0.1,
                        legend=dict(
                            orientation="h",
                            y=-0.2,
                            x=0
                        ),
            yaxis=dict(
                title=dict(text="Uang dalam USD"),
                side="left",
            ),
            yaxis2=dict(
                title=dict(text="Populasi Pemuda"),
                side="right",
                overlaying="y",
                tickmode="sync",
            ),
        )
        fig11.update_traces(texttemplate='%{text:.3s}')
        st.plotly_chart(fig11, use_container_width=True)

    st.subheader('Kesimpulan')
    st.markdown(p_format+
                'Berdasarkan analisis sederhana yang saya lakukan, dapat disimpulakan bahwa banyaknya biaya pendidikan yang dikeluarkan oleh pemerintah '\
                'tidak dapat dijadikan tolak ukur untuk menilai kualitas pendidikan. <b>Pendidikan yang dapat '\
                'di rasakan oleh orang-orang yang berhak dapat menjadi salah satu nilai kualitas pendidikan disuatu negara.</b> Namun, perlu lebih banyak data dari indikator '\
                'maupun variable lain untuk bisa menilai lebih dalam kualitas pendidikan.', unsafe_allow_html=True)
    st.markdown("---")  
    st.markdown("<b>Sumber : </b>", unsafe_allow_html=True)
    st.markdown("WBGAPI python package, data.worldbank.org/")   
    st.markdown("worldpopulationreview.com/country-rankings/average-iq-by-country", unsafe_allow_html=True) 
    st.markdown("genderdata.worldbank.org/topics/youth-15-24/", unsafe_allow_html=True)
    
      

# Halaman Country
if menu_id == 'by Country':
    #   Data BY COUNTRY
    df_country = df_main[['Year', 'PDB dalam USD', 'Pertumbuhan pendapatan negara',
       'Durasi Wajib Belajar',
       'Total Populasi', 'Nama Negara',
       'Total pengeluaran pemerintah untuk pendidikan',
       'Total pengeluaran pemerintah SELAIN pendidikan','Total Youth',
       'Total of youth not in education, employment or training']]
    st.title("Dashboard berdasarkan Negara")
    col1,col2 = st.columns([1,4])
    with col1:
        clist = list(df_country['Nama Negara'].unique())

        countries = st.multiselect("Pilih Negara", clist, default=['Indonesia','Malaysia'])

        indicators = list(df_country.select_dtypes(include=['int16', 'int32', 'int64', 'float16', 'float32', 'float64']))
        indicator = st.selectbox('Pilih Indikator', indicators)

    with col2:
        dfs = {country: df_country[df_country["Nama Negara"] == country] for country in countries}

        fig = go.Figure()
        for country, df in dfs.items():
            fig = fig.add_trace(go.Scatter(x=df["Year"].tolist(), y=df[indicator], name=country))

        st.plotly_chart(fig)
        # st.altair_chart(negara_line,use_container_width=True)

# Halaman Indikator
if menu_id == 'by Indicator':
    # Data BY INDIKATOR
    df_indicator = df_main[['Rank IQ', 'Year', 'PDB dalam USD', 'Pertumbuhan pendapatan negara',
       'Durasi Wajib Belajar',
       'Total Populasi', 'Nama Negara',
       'Total pengeluaran pemerintah untuk pendidikan',
       'Total pengeluaran pemerintah SELAIN pendidikan','Total Youth',
       'Total of youth not in education, employment or training']].sort_values('Rank IQ')
    st.title("Dashboard berdasarkan Indikator")
    col1,col2 = st.columns([1,4])
    with col1:
        years = list(df_indicator['Year'].unique())
        year = st.selectbox('Pilih Tahun', years)

        df_indi1 = df_indicator.drop('Rank IQ', axis=1)
        indicators_1 = list(df_indi1.select_dtypes(include=['int16', 'int32', 'int64', 'float16', 'float32', 'float64']))
        indicator_1 = st.selectbox('Indikator', indicators_1)

    with col2:
        cola, colb, colc= st.columns(3)
        # MAX
        max = df_indi1[df_indi1['Year']==year][['Nama Negara', indicator_1]].sort_values(indicator_1)[-1:]
        negara_max = max.iloc[0]['Nama Negara']
        value_max = numerize.numerize(float(max.iloc[0][indicator_1]))
        cola.metric("Tertinggi", negara_max, value_max)

        # MIN
        min = df_indi1[df_indi1['Year']==year][['Nama Negara', indicator_1]].sort_values(indicator_1)[:1]
        negara_min = min.iloc[0]['Nama Negara']
        value_min = numerize.numerize(float(min.iloc[0][indicator_1]))
        colb.metric("Terendah", negara_min, value_min, delta_color="inverse")

        # AVG
        avg_1 = numerize.numerize(float(np.nanmean(df_indi1[df_indi1['Year']==year][indicator_1])))
        colc.metric("Rata-Rata", avg_1)

        indi_bar = px.bar(df_indi1[df_indi1['Year']==year], x='Nama Negara', y=indicator_1)

        # Garis Rata2
        indi_bar.add_hline(y=np.nanmean(df_indi1[df_indi1['Year']==year][indicator_1]), line_color="red")

        # Show Chart
        st.plotly_chart(indi_bar, use_container_width=True)

# Halaman Info
if menu_id == 'Info':
    # st.header('Author')
    p1,p2,p3= st.columns([2,4,2])
    with p2:
        st.markdown(p_format+
                    'Hallo! Aku <b>Silvia Atika Anggrayni</b>. Terima kasih sudah mengunjungi halaman project ini. '\
                    'Project ini dibangun untuk memenuhi Tugas Capstone Project dari Program <b>DQLab Tetris Batch 3</b>. '\
                    'Saat ini aku masih awam dalam bidang Data Analyst, saran dan kritikan akan sangat membantuku untuk bisa menjadi lebih baik kedepannya.'\
                    'Penulis bisa dihubungi melalui kontak dibawah ini.', unsafe_allow_html=True)
        
        contact1, contact2 = st.columns([2,15])
        with contact1:
            st.image("https://cdn-icons-png.flaticon.com/512/732/732026.png", width=40)
            st.image('https://cdn-icons-png.flaticon.com/512/49/49656.png', width=40)
            st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Octicons-mark-github.svg/2048px-Octicons-mark-github.svg.png', width=40)

        with contact2:
            st.subheader('silviatika.saa@gmail.com')
            st.subheader('linkedin.com/in/silvia-saa/')
            st.subheader('github.com/slvsaa')