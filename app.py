
import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Hotspot Jambi 2018–2023",
    page_icon="🔥",
    layout="wide"
)

st.markdown("""
<style>
    .main-title {
        font-size: 2rem;
        font-weight: 700;
        color: #FF4500;
        text-align: center;
    }
    .sub-title {
        font-size: 1rem;
        color: #888;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .metric-box {
        background: #1e1e1e;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border-left: 4px solid #FF4500;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df       = pd.read_csv("data_processed/hotspot_jambi_clean.csv")
    df_bulan = pd.read_csv("data_processed/hotspot_per_bulan.csv")
    df_tahun = pd.read_csv("data_processed/hotspot_per_tahun.csv")
    df_kluster = pd.read_csv("data_processed/cluster_summary2.csv")
    df['acq_date'] = pd.to_datetime(df['acq_date'])
    # Merge nama daerah ke df utama
    df = df.merge(df_kluster[['cluster','nama_daerah']], on='cluster', how='left')
    df['nama_daerah'] = df['nama_daerah'].fillna('Noise/Outlier')
    return df, df_bulan, df_tahun, df_kluster

df, df_bulan, df_tahun, df_kluster = load_data()

st.markdown('<div class="main-title">🔥 Visualisasi Spasio-Temporal Titik Panas (Hotspot)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Pola Sebaran Kebakaran Hutan dan Lahan di Provinsi Jambi (2018–2023) | Data: NASA FIRMS MODIS</div>', unsafe_allow_html=True)
st.divider()

st.sidebar.header(" Filter Data")

tahun_list = sorted(df['year'].unique())
tahun_pilih = st.sidebar.multiselect(
    "Pilih Tahun",
    options=tahun_list,
    default=tahun_list
)

bulan_nama = ['January','February','March','April','May','June',
              'July','August','September','October','November','December']
bulan_pilih = st.sidebar.multiselect(
    "Pilih Bulan",
    options=bulan_nama,
    default=bulan_nama
)

mode_peta = st.sidebar.selectbox(
    "Mode Tampilan Peta",
    ["Heatmap", "Marker Kluster", "Kluster DBSCAN"]
)

min_conf = st.sidebar.slider("Minimum Confidence (%)", 30, 100, 50)

st.sidebar.divider()
st.sidebar.markdown("**ℹ️ Tentang Aplikasi**")
st.sidebar.markdown("Aplikasi ini memvisualisasikan sebaran titik panas di Provinsi Jambi berdasarkan data satelit MODIS NASA, dilengkapi analisis kluster DBSCAN untuk mengidentifikasi zona rawan karhutla.")

df_f = df[
    (df['year'].isin(tahun_pilih)) &
    (df['month_name'].isin(bulan_pilih)) &
    (df['confidence'] >= min_conf)
]

# ── METRIK RINGKASAN ──────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("🔥 Total Hotspot", f"{len(df_f):,}")
col2.metric("📅 Tahun Terpilih", f"{len(tahun_pilih)}")
col3.metric("🌡️ Avg Brightness", f"{df_f['brightness'].mean():.1f} K" if len(df_f) > 0 else "—")
col4.metric("⚡ Avg FRP", f"{df_f['frp'].mean():.1f} MW" if len(df_f) > 0 else "—")

st.divider()

col_map, col_chart = st.columns([3, 2])

with col_map:
    st.subheader("🗺️ Peta Sebaran Hotspot")

    if len(df_f) == 0:
        st.warning("Tidak ada data untuk filter yang dipilih.")
    else:
        m = folium.Map(
            location=[-1.5, 102.8],
            zoom_start=7,
            tiles="CartoDB dark_matter"
        )

        folium.Rectangle(
            bounds=[[-3.0, 101.5], [0.0, 104.7]],
            color="#FF4500",
            fill=False,
            weight=1.5,
            dash_array="5 5",
            tooltip="Bounding Box Provinsi Jambi"
        ).add_to(m)

        if mode_peta == "Heatmap":
            heat_data = df_f[['latitude', 'longitude', 'frp']].values.tolist()
            HeatMap(
                heat_data,
                min_opacity=0.3,
                max_zoom=10,
                radius=12,
                blur=15,
                gradient={0.2: 'blue', 0.45: 'lime', 0.7: 'orange', 1.0: 'red'}
            ).add_to(m)

            legend_html = """
            <div style="position:fixed;bottom:30px;left:30px;z-index:1000;
                        background:rgba(0,0,0,0.7);padding:10px;border-radius:8px;
                        color:white;font-size:12px;">
                <b>🔥 Intensitas FRP</b><br>
                <span style="color:#0000ff">■</span> Rendah &nbsp;
                <span style="color:#00ff00">■</span> Sedang &nbsp;
                <span style="color:#ffa500">■</span> Tinggi &nbsp;
                <span style="color:#ff0000">■</span> Ekstrem
            </div>"""
            m.get_root().html.add_child(folium.Element(legend_html))

        elif mode_peta == "Marker Kluster":
            mc = MarkerCluster(name="Hotspot Cluster").add_to(m)
            sample = df_f.sample(min(2000, len(df_f)), random_state=42)
            for _, row in sample.iterrows():
                folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=4,
                    color='#FF4500',
                    fill=True,
                    fill_opacity=0.7,
                    popup=folium.Popup(
                        f"<b>📍 Daerah:</b> {row['nama_daerah']}<br>"
                        f"<b>🔢 Kluster:</b> {label}<br>"
                        f"<b>📅 Tanggal:</b> {row['acq_date'].date()}<br>"
                        f"<b>⚡ FRP:</b> {row['frp']} MW<br>"
                        f"<b>✅ Confidence:</b> {row['confidence']}%",
                        max_width=200
                    )
                ).add_to(mc)

        elif mode_peta == "Kluster DBSCAN":
            colors = px.colors.qualitative.Set1
            top_clusters = df_f[df_f['cluster'] >= 0]['cluster'].value_counts().head(10).index.tolist()

            for _, row in df_f.iterrows():
                if row['cluster'] == -1:
                    color = '#888888'
                    label = "Noise"
                elif row['cluster'] in top_clusters:
                    color = colors[top_clusters.index(row['cluster']) % len(colors)]
                    label = f"Kluster {row['cluster']}"
                else:
                    color = '#FFAA00'
                    label = f"Kluster {row['cluster']}"

                folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=3,
                    color=color,
                    fill=True,
                    fill_opacity=0.6,
                    popup=folium.Popup(
                        f"<b>Kluster:</b> {label}<br>"
                        f"<b>📅 Tanggal:</b> {row['acq_date'].date()}<br>"
                        f"<b>⚡ FRP:</b> {row['frp']} MW<br>"
                        f"<b>✅ Confidence:</b> {row['confidence']}%",
                        max_width=180
                    )
                ).add_to(m)

            legend_html = """
            <div style="position:fixed;bottom:30px;left:30px;z-index:1000;
                        background:rgba(0,0,0,0.7);padding:10px;border-radius:8px;
                        color:white;font-size:12px;">
                <b>🤖 Kluster DBSCAN</b><br>
                <span style="color:#e41a1c">■</span> Kluster Utama<br>
                <span style="color:#ffaa00">■</span> Kluster Lain<br>
                <span style="color:#888">■</span> Noise/Outlier
            </div>"""
            m.get_root().html.add_child(folium.Element(legend_html))

        folium.LayerControl().add_to(m)
        st_folium(m, width=700, height=500)

with col_chart:
    st.subheader("📊 Tren Temporal")

    df_tahun_f = df_f.groupby('year').size().reset_index(name='count')
    fig_tahun = px.bar(
        df_tahun_f,
        x='year', y='count',
        color='count',
        color_continuous_scale='YlOrRd',
        title='Jumlah Hotspot per Tahun',
        labels={'year': 'Tahun', 'count': 'Jumlah Hotspot'}
    )
    fig_tahun.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        showlegend=False,
        height=250,
        margin=dict(t=40, b=20, l=20, r=20)
    )
    st.plotly_chart(fig_tahun, use_container_width=True)

    df_bulan_f = df_f.groupby('month').size().reset_index(name='count')
    bulan_order = list(range(1, 13))
    bulan_label = ['Jan','Feb','Mar','Apr','Mei','Jun','Jul','Agu','Sep','Okt','Nov','Des']
    df_bulan_f['bulan_label'] = df_bulan_f['month'].apply(lambda x: bulan_label[x-1])

    fig_bulan = px.line(
        df_bulan_f,
        x='month', y='count',
        markers=True,
        title='Distribusi Hotspot per Bulan',
        labels={'month': 'Bulan', 'count': 'Jumlah Hotspot'},
        color_discrete_sequence=['#FF4500']
    )
    fig_bulan.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=250,
        margin=dict(t=40, b=20, l=20, r=20)
    )
    fig_bulan.update_xaxes(tickvals=list(range(1,13)), ticktext=bulan_label)
    st.plotly_chart(fig_bulan, use_container_width=True)

st.divider()

st.subheader("Hasil Analisis Kluster DBSCAN")
col_a, col_b = st.columns(2)

with col_a:
    top10 = df_kluster.nlargest(10, 'jumlah_titik').copy()
    top10['cluster'] = top10['cluster'].astype(str)
    fig_cluster = px.bar(
        top10,
        x='cluster', y='jumlah_titik',
        color='avg_frp',
        color_continuous_scale='YlOrRd',
        title='Top 10 Kluster Terbesar',
        labels={'cluster': 'ID Kluster', 'jumlah_titik': 'Jumlah Titik', 'avg_frp': 'Avg FRP (MW)'}
    )
    fig_cluster.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=300,
        margin=dict(t=40, b=20, l=20, r=20)
    )
    st.plotly_chart(fig_cluster, use_container_width=True)

with col_b:
    st.markdown("**📋 Ringkasan Kluster DBSCAN**")
    n_kluster  = len(df_kluster)
    n_noise    = (df['cluster'] == -1).sum()
    n_terbesar = df_kluster['jumlah_titik'].max()
    kluster_id = df_kluster.loc[df_kluster['jumlah_titik'].idxmax(), 'cluster']

    st.markdown(f"""
    | Metrik | Nilai |
    |---|---|
    | Total kluster ditemukan | **{n_kluster}** |
    | Titik noise/outlier | **{n_noise:,}** |
    | Kluster terbesar (ID {kluster_id}) | **{n_terbesar:,} titik** |
    | Algoritma | **DBSCAN** |
    | Parameter eps | **0.05°** (~5.5 km) |
    | Min samples | **5 titik** |
    """)

    st.info("Kluster besar menunjukkan zona konsentrasi karhutla yang perlu prioritas mitigasi.")

st.divider()

with st.expander("📄 Lihat Data Mentah (sample 500 baris)"):
    st.dataframe(
        df_f.sample(min(500, len(df_f)), random_state=42)[[
            'acq_date','latitude','longitude',
            'brightness','frp','confidence',
            'year','month_name','cluster_label','nama_daerah'
        ]].sort_values('acq_date'),
        use_container_width=True
    )

st.markdown("---")
st.markdown(
    "<center><small>Data: NASA FIRMS MODIS C6.1 | Analisis: DBSCAN Clustering | "
    "Visualisasi: Streamlit + Folium + Plotly</small></center>",
    unsafe_allow_html=True
)
