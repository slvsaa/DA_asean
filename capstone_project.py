# Import Library
import streamlit as st
import pandas as pd
import numpy as np
import hydralit_components as hc
import plotly.express as px
import plotly.graph_objects as go
import altair as alt

# import wbgapi as wb

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

# Halaman Home
# if menu_id == 'Home':
#     st.write('Hallo Saya Silvia')


# Halaman Country
if menu_id == 'by Country':
    st.title("Dashboard berdasarkan Country")
    col1,col2 = st.columns([1,4])
    with col1:
        countries = list(df_main['Nama Negara'].unique())
        country = st.selectbox('Choose Country', countries)

        # country = st.multiselect(
        #     label="Select neighbourhood average price you want to visualize", options=countries,
        #     default=["Indonesia", 'Singapore'], max_selections=11)

        # if not country:
        #     st.warning('At least you must select one option')

        indicators = list(df_main.select_dtypes(include=['int16', 'int32', 'int64', 'float16', 'float32', 'float64']))
        indicator = st.selectbox('Choose Indicator', indicators)

    with col2:
        negara_line = alt.Chart(df_main[df_main['Nama Negara'] == country]).mark_line().encode(
            alt.X('Year', title='Year'),
            alt.Y(indicator, title='Indicator')
        )

        st.altair_chart(negara_line,use_container_width=True)

# Halaman Indikator
if menu_id == 'by Indicator':
    st.title("Dashboard berdasarkan Indikator")
    col1,col2 = st.columns([1,4])
    with col1:
        years = list(df_main['Year'].unique())
        year = st.selectbox('Choose Indicator', years)

        indicators = list(df_main.select_dtypes(include=['int16', 'int32', 'int64', 'float16', 'float32', 'float64']))
        indicator = st.selectbox('Choose Indicator', indicators)

    with col2:
        indi_bar = alt.Chart(df_main[df_main['Year']==year].sort_values('Rank IQ')).mark_bar().encode(
            alt.X('Nama Negara', title='Nama Negara', sort=None),
            alt.Y(indicator, title='Indicator')
        )

        st.altair_chart(indi_bar,use_container_width=True)

# Halaman Analisis
if menu_id == 'Home':
    st.title('Pendidikan di Negara-Negara ASEAN')
    st.text("by Silvia Atika Anggrayni")
    st.markdown("---")

    p_format = '<p style="color:Black; font-size: 16px; text-align: justify">'
    st.markdown(p_format+
                '<b>Pada awal tahun 2023, World Population Review memaparkan Rata-Rata IQ berdasarkan Negara pada lamannya. </b>'\
                'IQ atau Intelligence Quotient merupakana salah satu tolak ukur untuk menilai kecerdasan seseorang dengan cara '\
                'mengikuti tes, semakin tinggi angkanya maka semakin tinggi pula kecerdasan orang tersebut. '\
                'Indoensia sendiri mendapat peringkat 130 dari seluruh negara dengan Rata-Rata IQ 78,49. ', unsafe_allow_html=True)
    st.subheader('Bagaimana peringkat Indonesia di antara negara di ASEAN?')

    col1,col2 = st.columns([1,1])
    with col1:
        st.markdown(p_format+
                '<b>Diagram Rata-Rata IQ di ASEAN</b> menunjukkan Rata-rata IQ di ASEAN yang sudah diurutkan. '\
                'Dapat dilihat bahwa Indonesia berada diperingkat 2 terakhir dengan Singapura berada diperingkat teratas dan Timor Leste berada diperingkat terakhir di ASEAN. '\
                'Timor Leste berada diperingkat terakhir namun IQ yang dimiliki sama dengan Indonesia.' ,unsafe_allow_html=True)
        
        st.markdown(p_format+
                '<b>Dilansir dari World Population Review</b>, Skor IQ dapat mencerminkan kualitas pendidikan dan sumber daya yang dimiliki seseorang. '\
                'Maka dengan melihat Rata-Rata IQ di suatu negara, kita juga dapat menilai kualitas pendidikan di negara tersebut. '\
                'Wilayah dengan skor IQ rendah biasanya lebih miskin dan kurang berkembang, khususnya di bidang pendidikan, '\
                'dibandingkan dengan negara yang memiliki skor IQ yang tinggi. ',unsafe_allow_html=True)
        st.markdown(p_format+
                'Dengan adanya pernyataan tersebut, <b>apakah kualitas pendidikan Indonesia termasuk buruk dibanding dengan negara ASEAN lainnya berdasarkan kriteria? </b>'\
                'Analisis berikut akan melihat bagaimana pemerintah Indonesia mengalokasikan dana untuk pendidikan di negaranya, dibandingkan dengan negara ASEAN lainnya',unsafe_allow_html=True)
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
    df_combo2 = df_main[['Rank IQ','Nama Negara', 'PDB dalam USD','Year', 'Total pengeluaran pemerintah untuk pendidikan',
                         'Total Populasi','Pengeluaran pemerintah untuk pendidikan, total (% dari PDB)']].sort_values('Rank IQ')
    
    cold,cole= st.columns([1,3])
    with cold:
        years_1 = list(df_main['Year'].unique())
        year_1 = st.selectbox('Pilih', years_1)

    fig12 = go.Figure(data=[
        go.Bar(name='PDB dalam USD', 
               x=df_combo2[df_combo2['Year']==year_1]['Nama Negara'], 
                y=df_combo2[df_combo2['Year']==year_1]['PDB dalam USD'],
                text=df_combo2[df_combo2['Year']==year_1]['PDB dalam USD']),
        go.Bar(name='Pengeluaran Pendidikan', 
                x=df_combo2[df_combo2['Year']==year_1]['Nama Negara'], 
                y=df_combo2[df_combo2['Year']==year_1]['Total pengeluaran pemerintah untuk pendidikan'],
                text=df_combo2[df_combo2['Year']==year_1]['Total pengeluaran pemerintah untuk pendidikan'],
                hovertext=round(df_combo2[df_combo2['Year']==year_1]['Pengeluaran pemerintah untuk pendidikan, total (% dari PDB)'],2),
                hovertemplate ='%{hovertext}%'
        ),
    ])
    fig12.add_trace(
            go.Scatter(
                x=df_combo2[df_combo2['Year']==year_1]['Nama Negara'],
                y=df_combo2[df_combo2['Year']==year_1]['Total Populasi'],
                yaxis="y2",
                name="Total Populasi",
        )
    )

    fig12.update_layout(
        title_text='Perbandingan PDB dan Pengeluaran Pendidikan', 
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

    # Rata-Rata PDB
    # avg_pdb = np.nanmean(df_combo2[df_combo2['Year']==year_1]['PDB dalam USD'])
    # fig12.add_hline(y=avg_pdb, line_color="red")
    # fig12.add_annotation(text='PDB AVG '+ str(round(avg_pdb/1000000000,2)) + ' Billion',
    #                         y=avg_pdb+40000000000, x=1.5, showarrow=False)
    # fig12.update_annotations(font=dict(size=14, color="red"))

    # Rata-Rata Pendidikan
    # avg_pendidikan = np.nanmean(df_combo2[df_combo2['Year']==year_1]['Total pengeluaran pemerintah untuk pendidikan'])
    # fig12.add_hline(y=avg_pendidikan, line_color="red")
    # fig12.add_annotation(text='Pengeluaran Pendidikan AVG '+ str(round(avg_pendidikan/1000000000,2)) + ' Billion',
    #                         y=avg_pendidikan+40000000000, x=1.5, showarrow=False)
    # fig12.update_annotations(font=dict(size=14, color="red"))

    # Change the bar mode
    fig12.update_layout(barmode='group')
    st.plotly_chart(fig12, use_container_width=True)

    st.markdown(p_format+
                'Dilihat dari nominal, pengeluaran pemerintah untuk pendidikan di Indonesia lebih besar dibanding negara lainnya.'\
                'Namun, bila dilihat dari presentase-nya, biaya pendidikan yang diambil dr PBD masing-masing tidak terlalu beda jauh,'\
                'yaitu 2-5%', unsafe_allow_html=True)
    
    # Pemuda
    st.subheader('Populasi Pemuda yang tidak sekolah, kerja, maupun pelatihan')
    cola,colb,colc = st.columns([1,2,1])
    # Data chart 2
    df_combo = df_main[['Rank IQ','Nama Negara', 'Total of youth not in education, employment or training','Year', 
                            'Total pengeluaran pemerintah untuk pendidikan','Total Youth',
                            'Share of youth not in education, employment or training, total (% of youth population)']].sort_values('Rank IQ')
    with colb:
        years = list(df_main['Year'].unique())
        year = st.selectbox('Choose Year', years)

    col5,col6 = st.columns([1,1])
    with col5:
        st.markdown(p_format+
                'Diagram disamping menunjukkan perbandingan total pemuda seluruhnya dengan total pemuda yang tidak sekolah, kerja, maupun mengikuti pelatihan '\
                'Jika dilihat dari diagram, jumlah pemuda tidak bersekolah palinga banyak berada di Indonesia. Namun, jika memerhatikan besarnya '\
                'presentase setiap negara, Timor Leste memiliki 30% keatas Pemuda tidak sekolah dari total pemuda yang berada di Timor Leste', unsafe_allow_html=True)

        st.markdown(p_format+
                'Jika dilihat lebih detail lagi, negara yang memiliki Rata-Rata IQ yang melebihi Rata-Rata IQ di ASEAN memiliki presentase kurang dari 20%'\
                'pemuda tidak bersekolah, sdangkan yang berada dibawah rata-rata mencapai 15-30% ', unsafe_allow_html=True)    
    with col6:
        fig11 = go.Figure(
            data=go.Bar(
                x=df_combo[df_combo['Year']==year]['Nama Negara'],
                y=df_combo[df_combo['Year']==year]['Total pengeluaran pemerintah untuk pendidikan'],
                name="Pengeluaran Pendidikan",
                text=df_combo[df_combo['Year']==year]['Total pengeluaran pemerintah untuk pendidikan']
                # marker=dict(color="paleturquoise"),
            )
        )

        fig11.add_trace(
            go.Scatter(
                x=df_combo[df_combo['Year']==year]['Nama Negara'],
                y=df_combo[df_combo['Year']==year]['Total of youth not in education, employment or training'],
                yaxis="y2",
                name="Pemuda Tidak sekolah",
                hovertext=round(df_combo[df_combo['Year']==year]['Share of youth not in education, employment or training, total (% of youth population)'],2),
                hovertemplate ='%{hovertext}%'
            )
        )

        fig11.add_trace(
            go.Scatter(
                x=df_combo[df_combo['Year']==year]['Nama Negara'],
                y=df_combo[df_combo['Year']==year]['Total Youth'],
                yaxis="y2",
                name="Total pemuda",
                # marker=dict(color="crimson"),
            )
        )

        fig11.update_layout(
            title_text='Pengeluaran dan Total Pemuda yang Tidak Bersekolah', 
                        title_x=0.2,
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

st.markdown("---")
st.subheader('Kesimpulan')
st.markdown(p_format+
            'Berdasarkan analisis sederhana yang saya lakukan, dapat disimpulakan bahwa banyaknya biaya pendidikan yang dikeluarkan oleh pemerintah '\
            'tidak dapat dijadikan tolak ukur untuk menilai kualitas pendidikan. <b>Pendidikan yang tepat sasaran dan dapat '\
            'di rasakan oleh orang-orang yang berhak lah yg bisa menjadi nilai kualitas pendidikan disuatu negara.</b> Perlu lebih banyak data dari indikator '\
            'maupun variable lain untuk bisa menilai lebih dalam kualitas pendidikan.', unsafe_allow_html=True)   

    