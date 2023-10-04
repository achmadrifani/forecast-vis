import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import altair as alt
import folium
from datetime import datetime, timedelta


fname_dict ={'ACEH':"aceh", 'SUMATERA UTARA':'sumut', 'SUMATERA BARAT':'sumbar', 'RIAU':'riau','KEPULAUAN RIAU':'kepriau',
             'JAMBI':'jambi', 'BENGKULU':'bengkulu', 'SUMATERA SELATAN':'sumsel','KEPULAUAN BANGKA BELITUNG':'babel', 'LAMPUNG':'lampung',
             'DKI JAKARTA':'jakarta', 'BANTEN':'banten', 'JAWA BARAT':'jawabarat', 'JAWA TENGAH':'jawatengah', 'DAERAH ISTIMEWA YOGYAKARTA':'jogyakarta',
             'JAWA TIMUR':'jawatimur', 'KALIMANTAN BARAT':'kalbar', 'KALIMANTAN TENGAH':'kalteng', 'KALIMANTAN TIMUR':'kaltim',
             'KALIMANTAN SELATAN':'kalsel', "KALIMANTAN UTARA":'kaluta','BALI':'bali', 'NUSA TENGGARA BARAT':'ntb', 'NUSA TENGGARA TIMUR':'ntt', 'SULAWESI UTARA':'sulut', 'GORONTALO':'gorontalo',
             'SULAWESI TENGAH':'sulteng', 'SULAWESI BARAT':'sulbar', 'SULAWESI SELATAN':'sulsel','SULAWESI TENGGARA':'sultenggara',
             'MALUKU':'maluku', 'MALUKU UTARA':'malut', 'PAPUA':'papua','PAPUA BARAT':'papuabarat'}
prov_list = ['ACEH', 'SUMATERA UTARA', 'SUMATERA BARAT', 'RIAU','KEPULAUAN RIAU',
             'JAMBI', 'BENGKULU', 'SUMATERA SELATAN','KEPULAUAN BANGKA BELITUNG', 'LAMPUNG',
             'DKI JAKARTA', 'BANTEN', 'JAWA BARAT', 'JAWA TENGAH', 'DAERAH ISTIMEWA YOGYAKARTA',
             'JAWA TIMUR', 'KALIMANTAN BARAT', 'KALIMANTAN TENGAH', 'KALIMANTAN TIMUR',
             'KALIMANTAN SELATAN', "KALIMANTAN UTARA",'BALI', 'NUSA TENGGARA BARAT', 'NUSA TENGGARA TIMUR', 'SULAWESI UTARA', 'GORONTALO',
             'SULAWESI TENGAH', 'SULAWESI BARAT', 'SULAWESI SELATAN','SULAWESI TENGGARA',
             'MALUKU', 'MALUKU UTARA', 'PAPUA','PAPUA BARAT']
wx_icon_dict = {0:"https://www.bmkg.go.id/asset/img/weather_icon/ID/cerah-am.png",
                1:"https://www.bmkg.go.id/asset/img/weather_icon/ID/cerah%20berawan-am.png",
                2:"https://www.bmkg.go.id/asset/img/weather_icon/ID/cerah%20berawan-am.png",
                3:"https://www.bmkg.go.id/asset/img/weather_icon/ID/berawan-am.png",
                4:"https://www.bmkg.go.id/asset/img/weather_icon/ID/berawan tebal-am.png",
                10:"https://www.bmkg.go.id/asset/img/weather_icon/ID/asap-am.png",
                45:"https://www.bmkg.go.id/asset/img/weather_icon/ID/kabut-am.png",
                60:"https://www.bmkg.go.id/asset/img/weather_icon/ID/hujan%20ringan-am.png",
                61:"https://www.bmkg.go.id/asset/img/weather_icon/ID/hujan%20sedang-am.png",
                63:"https://www.bmkg.go.id/asset/img/weather_icon/ID/hujan%20lebat-am.png",
                95:"https://www.bmkg.go.id/asset/img/weather_icon/ID/hujan%20petir-am.png",
                97:"https://www.bmkg.go.id/asset/img/weather_icon/ID/hujan%20petir-am.png"}
wx_caption_dict = {0:"Cerah",
                1:"Cerah Berawan",
                2:"Cerah Berawan",
                3:"Berawan",
                4:"Berawan Tebal",
                10:"Asap",
                45:"Kabut",
                60:"Hujan Ringan",
                61:"Hujan Sedang",
                63:"Hujan Lebat",
                95:"Hujan Petir",
                97:"Hujan Petir"}
wind_caption_dict = {"N":"Utara",
                     "NE":"Timur Laut",
                     "E":"Timur",
                     "SE":"Tenggara",
                     "S":"Selatan",
                     "SW":"Barat Daya",
                     "W":"Barat",
                     "NW":"Barat Laut"}

def load_df(prov):
    df = pd.read_csv(f"http://202.90.198.220/MEWS/CSV/kecamatanforecast-{prov}.csv", sep=";",
                     names=["area_id", "time", "tmin", "tmax", "humin", "humax", "hu", "t", "weather", "wd", "ws"],
                     parse_dates=["time"])
    df_geo = pd.read_csv(f"kecamatan_geofeatures.csv", sep=";",
                         names=["area_id", "kec", "kab", "prov", "lat", "lon"])
    df = pd.merge(df, df_geo, how="inner", on="area_id")

    return df


st.set_page_config(layout="wide")
st.header("BMKG Forecast")
st.write("Visualisasi Forecast BMKG")

col1,col2,col3 = st.columns([0.3,0.1,0.4],gap='medium')

with col1:
    prov_select = st.selectbox('Provinsi',prov_list,index=None, placeholder="Pilih Provinsi ...")

    if prov_select is not None:
        prov = fname_dict[prov_select]
        df = load_df(prov)
        kab_list = df["kab"].unique()
        kab_sel = st.selectbox('Kabupaten / Kota', kab_list, index=None, placeholder="Pilih Kabupaten / Kota ...")
        kec_list = df["kec"].loc[df["kab"]==kab_sel].unique()
        kec_sel = st.selectbox('Kecamatan', kec_list, index=None, placeholder="Pilih Kecamatan ...")
    else:
        kab_sel = st.selectbox('Kabupaten / Kota', ('...'), index=None, placeholder="Pilih Kabupaten / Kota ...")
        kec_sel = st.selectbox('Kecamatan', ('...'), index=None, placeholder="Pilih Kecamatan ...")

    if kab_sel:
        df_kab_sel = df.loc[df["kab"] == kab_sel]


if kec_sel is not None:
    st.write("## Prakiraan Cuaca")
    df_kec_sel = df_kab_sel.loc[df_kab_sel["kec"] == kec_sel]

    df_grp = df_kec_sel.groupby(by=df["time"].dt.date)
    tanggal_list = list(df_grp.groups.keys())
    tanggal_list_string = [x.strftime("%d / %m") for x in tanggal_list]
    tabs = st.tabs(tanggal_list_string)
    for tab,tanggal in zip(tabs,tanggal_list):
        df_tgl = df_grp.get_group(tanggal)
        cols = tab.columns(df_tgl.shape[0])
        for col,(index,data) in zip(cols,df_tgl.iterrows()):
            col.write((data["time"]+timedelta(hours=7)).strftime("%H:%M WIB"))
            col.image(wx_icon_dict[data['weather']],width=50)
            col.write(wx_caption_dict[data["weather"]])
            col.text(f"Suhu: {data['t']} C")
            col.text(f"Kelembapan: {data['hu']} %")
            col.text(f"Angin: {wind_caption_dict[data['wd']]} \n{data['ws']} km/jam")

    st.write("## Grafik Temperatur")
    min_time, max_time = st.select_slider("Pilih Rentang Waktu", df_kec_sel["time"],
                                          value=(df_kec_sel["time"].iloc[0], df_kec_sel["time"].iloc[-1]))
    df_kec_sel = df_kec_sel.loc[(df_kec_sel["time"] >= min_time) & (df_kec_sel["time"] <= max_time)]
    tchart = alt.Chart(df_kec_sel).mark_line().encode(
        x='time:T',
        y=alt.Y('t:Q', scale=alt.Scale(domain=[15, 38]))
    ).properties(
        width=600,  # Lebar plot
        height=300  # Tinggi plot
    )
    st.altair_chart(tchart, use_container_width=True)
else:
    st.write("## Prakiraan Cuaca")
    st.write("## Grafik Temperatur")

with col3:
    if kec_sel:
        # Inisialisasi peta menggunakan Folium
        lon,lat = df_kec_sel["lon"].iloc[0],df_kec_sel["lat"].iloc[0]
        m = folium.Map(location=[lat,lon], zoom_start=13)  # Koordinat awal dan level zoom
        # Tambahkan tanda (marker) ke peta
        folium.Marker([lat,lon], tooltip=kec_sel).add_to(m)
        st_map = st_folium(m, width=300, height=300)
    else:
        m = folium.Map(location=[-2.4833826,117.8902853], zoom_start=5)  # Koordinat awal dan level zoom
        # Tambahkan tanda (marker) ke peta
        st_map = st_folium(m, width=300, height=300)


