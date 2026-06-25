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
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0a0a0f 0%, #0f0f1a 50%, #0a0f0a 100%);
    color: #e8e8e8;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; }

.hero-wrap {
    background: linear-gradient(135deg, rgba(255,69,0,0.12) 0%, rgba(255,140,0,0.06) 50%, rgba(0,0,0,0) 100%);
    border: 1px solid rgba(255,69,0,0.2);
    border-radius: 16px;
    padding: 2rem 2.5rem 1.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(255,69,0,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,69,0,0.15);
    border: 1px solid rgba(255,69,0,0.4);
    color: #FF6B35;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 0.75rem;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.2;
    margin: 0.3rem 0 0.5rem;
    letter-spacing: -0.02em;
}
.hero-title span { color: #FF4500; }
.hero-sub {
    font-size: 0.9rem;
    color: #9a9aaa;
    font-weight: 400;
    margin: 0;
}
.hero-sub b { color: #ccccdd; }

.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 1.5rem;
}
.metric-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1.1rem 1.2rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: rgba(255,69,0,0.3); }
.metric-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0;
    width: 100%; height: 2px;
    background: linear-gradient(90deg, #FF4500, transparent);
}
.metric-icon { font-size: 1.4rem; margin-bottom: 0.4rem; }
.metric-val {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #ffffff;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.metric-label {
    font-size: 0.75rem;
    color: #7a7a8a;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 500;
}

.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}
.section-icon {
    width: 32px; height: 32px;
    background: rgba(255,69,0,0.15);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
}
.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #e8e8e8;
    margin: 0;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d18 0%, #0a0a12 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown p {
    color: #ccccdd !important;
}
.sidebar-brand {
    background: linear-gradient(135deg, rgba(255,69,0,0.15), rgba(255,140,0,0.08));
    border: 1px solid rgba(255,69,0,0.25);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin-bottom: 1.2rem;
    text-align: center;
}
.sidebar-brand-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.85rem;
    font-weight: 700;
    color: #FF6B35;
    letter-spacing: 0.05em;
}
.sidebar-brand-sub {
    font-size: 0.7rem;
    color: #7a7a8a;
    margin-top: 2px;
}
.info-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-left: 3px solid #FF4500;
    border-radius: 8px;
    padding: 0.7rem 0.9rem;
    font-size: 0.78rem;
    color: #9a9aaa;
    line-height: 1.5;
    margin-top: 0.5rem;
}

.map-container {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1rem;
    height: 100%;
}

.stat-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-top: 1rem;
}
.stat-item {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    text-align: center;
}
.stat-num {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #FF6B35;
}
.stat-desc {
    font-size: 0.72rem;
    color: #7a7a8a;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}

.dbscan-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
}
.dbscan-table th {
    background: rgba(255,69,0,0.12);
    color: #FF6B35;
    font-weight: 600;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 0.6rem 0.8rem;
    border-bottom: 1px solid rgba(255,69,0,0.2);
    text-align: left;
}
.dbscan-table td {
    padding: 0.55rem 0.8rem;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    color: #ccccdd;
}
.dbscan-table tr:hover td { background: rgba(255,255,255,0.02); }
.badge-algo {
    display: inline-block;
    background: rgba(255,69,0,0.15);
    border: 1px solid rgba(255,69,0,0.3);
    color: #FF6B35;
    font-size: 0.7rem;
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: 600;
}

.js-plotly-plot { border-radius: 8px; overflow: hidden; }


.custom-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,69,0,0.3), transparent);
    margin: 1.5rem 0;
}


.footer-wrap {
    text-align: center;
    padding: 1.2rem;
    margin-top: 2rem;
    border-top: 1px solid rgba(255,255,255,0.06);
}
.footer-wrap span {
    font-size: 0.75rem;
    color: #555566;
    letter-spacing: 0.05em;
}
.footer-wrap b { color: #FF4500; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df         = pd.read_csv("data_processed/hotspot_jambi_clean.csv")
    df_bulan   = pd.read_csv("data_processed/hotspot_per_bulan.csv")
    df_tahun   = pd.read_csv("data_processed/hotspot_per_tahun.csv")
    df_kluster = pd.read_csv("data_processed/cluster_summary.csv")
    df['acq_date'] = pd.to_datetime(df['acq_date'])
    df = df.merge(df_kluster[['cluster', 'nama_daerah']], on='cluster', how='left')
    df['nama_daerah'] = df['nama_daerah'].fillna('Noise/Outlier')
    return df, df_bulan, df_tahun, df_kluster

df, df_bulan, df_tahun, df_kluster = load_data()



with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-title">🔥 HOTSPOT JAMBI</div>
        <div class="sidebar-brand-sub">Spasio-Temporal Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**🗓 Rentang Waktu**")
    tahun_list  = sorted(df['year'].unique())
    tahun_pilih = st.multiselect("Pilih Tahun", options=tahun_list, default=tahun_list, label_visibility="collapsed")

    st.markdown("**📅 Bulan**")
    bulan_nama  = ['January','February','March','April','May','June',
                   'July','August','September','October','November','December']
    bulan_pilih = st.multiselect("Pilih Bulan", options=bulan_nama, default=bulan_nama, label_visibility="collapsed")

    st.markdown("**🗺 Mode Peta**")
    mode_peta = st.selectbox("Mode", ["Heatmap", "Marker Kluster", "Kluster DBSCAN"], label_visibility="collapsed")

    st.markdown("**🎯 Confidence Level**")
    min_conf = st.slider("Min Confidence (%)", 30, 100, 50, label_visibility="collapsed")

    st.divider()
    st.markdown("""
    <div class="info-box">
        📡 Data bersumber dari <b>NASA FIRMS MODIS C6.1</b><br>
        🤖 Klusterisasi menggunakan <b>DBSCAN</b><br>
        📍 Wilayah: <b>Provinsi Jambi</b><br>
        📆 Periode: <b>2018 – 2023</b>
    </div>
    """, unsafe_allow_html=True)


df_f = df[
    (df['year'].isin(tahun_pilih)) &
    (df['month_name'].isin(bulan_pilih)) &
    (df['confidence'] >= min_conf)
]


st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">🛰 NASA FIRMS · MODIS C6.1 · Provinsi Jambi</div>
    <div class="hero-title">Visualisasi <span>Spasio-Temporal</span><br>Titik Panas Karhutla</div>
    <p class="hero-sub">Pola sebaran kebakaran hutan dan lahan di Provinsi Jambi periode <b>2018–2023</b> — dianalisis menggunakan klusterisasi <b>DBSCAN</b> dan divisualisasikan secara interaktif.</p>
</div>
""", unsafe_allow_html=True)


avg_br  = f"{df_f['brightness'].mean():.1f} K"  if len(df_f) > 0 else "—"
avg_frp = f"{df_f['frp'].mean():.1f} MW"        if len(df_f) > 0 else "—"
pct_19  = f"{len(df_f[df_f['year']==2019])/max(len(df_f),1)*100:.1f}%" if len(df_f) > 0 else "—"

st.markdown(f"""
<div class="metric-grid">
    <div class="metric-card">
        <div class="metric-icon">🔥</div>
        <div class="metric-val">{len(df_f):,}</div>
        <div class="metric-label">Total Hotspot</div>
    </div>
    <div class="metric-card">
        <div class="metric-icon">🌡️</div>
        <div class="metric-val">{avg_br}</div>
        <div class="metric-label">Avg Brightness</div>
    </div>
    <div class="metric-card">
        <div class="metric-icon">⚡</div>
        <div class="metric-val">{avg_frp}</div>
        <div class="metric-label">Avg FRP</div>
    </div>
    <div class="metric-card">
        <div class="metric-icon">📅</div>
        <div class="metric-val">{len(tahun_pilih)}</div>
        <div class="metric-label">Tahun Dipilih</div>
    </div>
</div>
""", unsafe_allow_html=True)


col_map, col_chart = st.columns([3, 2], gap="medium")

with col_map:
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🗺</div>
        <p class="section-title">Peta Sebaran Hotspot</p>
    </div>
    """, unsafe_allow_html=True)

    if len(df_f) == 0:
        st.warning("⚠️ Tidak ada data untuk filter yang dipilih. Coba ubah filter di sidebar.")
    else:
        m = folium.Map(
            location=[-1.5, 102.8],
            zoom_start=7,
            tiles="CartoDB dark_matter"
        )
        folium.Rectangle(
            bounds=[[-3.0, 101.5], [0.0, 104.7]],
            color="#FF4500", fill=False,
            weight=1.5, dash_array="6 4",
            tooltip="Bounding Box Provinsi Jambi"
        ).add_to(m)

        if mode_peta == "Heatmap":
            heat_data = df_f[['latitude', 'longitude', 'frp']].values.tolist()
            HeatMap(heat_data, min_opacity=0.3, max_zoom=10, radius=13, blur=16,
                    gradient={0.2:'blue', 0.45:'lime', 0.7:'orange', 1.0:'red'}).add_to(m)
            legend_html = """
            <div style="position:fixed;bottom:20px;left:20px;z-index:1000;
                        background:rgba(10,10,20,0.88);padding:10px 14px;
                        border-radius:10px;color:white;font-size:11px;
                        border:1px solid rgba(255,69,0,0.3);font-family:Inter,sans-serif;">
                <b style="color:#FF6B35;letter-spacing:.05em">INTENSITAS FRP</b><br><br>
                <span style="color:#4444ff">■</span>&nbsp;Rendah &nbsp;
                <span style="color:#00cc44">■</span>&nbsp;Sedang<br>
                <span style="color:#ff8800">■</span>&nbsp;Tinggi &nbsp;&nbsp;
                <span style="color:#ff2200">■</span>&nbsp;Ekstrem
            </div>"""
            m.get_root().html.add_child(folium.Element(legend_html))

        elif mode_peta == "Marker Kluster":
            mc = MarkerCluster(name="Hotspot Cluster").add_to(m)
            sample = df_f.sample(min(2000, len(df_f)), random_state=42)
            for _, row in sample.iterrows():
                folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=4, color='#FF4500', fill=True, fill_opacity=0.75,
                    popup=folium.Popup(
                        f"<div style='font-family:Inter,sans-serif;font-size:12px;min-width:180px'>"
                        f"<b style='color:#FF4500'>📍 {row['nama_daerah']}</b><br>"
                        f"<hr style='margin:4px 0;border-color:#eee'>"
                        f"<b>Kluster:</b> {row['cluster_label']}<br>"
                        f"<b>Tanggal:</b> {row['acq_date'].date()}<br>"
                        f"<b>Brightness:</b> {row['brightness']} K<br>"
                        f"<b>FRP:</b> {row['frp']} MW<br>"
                        f"<b>Confidence:</b> {row['confidence']}%</div>",
                        max_width=220
                    )
                ).add_to(mc)

        elif mode_peta == "Kluster DBSCAN":
            clr = px.colors.qualitative.Set1
            top_clusters = df_f[df_f['cluster'] >= 0]['cluster'].value_counts().head(10).index.tolist()
            for _, row in df_f.iterrows():
                if row['cluster'] == -1:
                    color, label = '#555566', 'Noise/Outlier'
                elif row['cluster'] in top_clusters:
                    color = clr[top_clusters.index(row['cluster']) % len(clr)]
                    label = f"Kluster {row['cluster']}"
                else:
                    color, label = '#FFAA00', f"Kluster {row['cluster']}"
                folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=3, color=color, fill=True, fill_opacity=0.65,
                    popup=folium.Popup(
                        f"<div style='font-family:Inter,sans-serif;font-size:12px;min-width:180px'>"
                        f"<b style='color:#FF4500'>📍 {row['nama_daerah']}</b><br>"
                        f"<hr style='margin:4px 0;border-color:#eee'>"
                        f"<b>Kluster:</b> {label}<br>"
                        f"<b>Tanggal:</b> {row['acq_date'].date()}<br>"
                        f"<b>FRP:</b> {row['frp']} MW<br>"
                        f"<b>Confidence:</b> {row['confidence']}%</div>",
                        max_width=210
                    )
                ).add_to(m)
            legend_html = """
            <div style="position:fixed;bottom:20px;left:20px;z-index:1000;
                        background:rgba(10,10,20,0.88);padding:10px 14px;
                        border-radius:10px;color:white;font-size:11px;
                        border:1px solid rgba(255,69,0,0.3);font-family:Inter,sans-serif;">
                <b style="color:#FF6B35;letter-spacing:.05em">KLUSTER DBSCAN</b><br><br>
                <span style="color:#e41a1c">■</span>&nbsp;Kluster Utama<br>
                <span style="color:#ffaa00">■</span>&nbsp;Kluster Lain<br>
                <span style="color:#555566">■</span>&nbsp;Noise/Outlier
            </div>"""
            m.get_root().html.add_child(folium.Element(legend_html))

        folium.LayerControl().add_to(m)
        st_folium(m, width=None, height=480, use_container_width=True)


with col_chart:
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">📊</div>
        <p class="section-title">Tren Temporal</p>
    </div>
    """, unsafe_allow_html=True)

    # Chart Tahunan
    df_tahun_f = df_f.groupby('year').size().reset_index(name='count')
    fig_tahun = px.bar(
        df_tahun_f, x='year', y='count',
        color='count', color_continuous_scale='YlOrRd',
        labels={'year': 'Tahun', 'count': 'Hotspot'},
        title='Jumlah Hotspot per Tahun'
    )
    fig_tahun.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#aaaacc', family='Inter', size=11),
        title=dict(font=dict(size=13, color='#e8e8e8')),
        showlegend=False, height=220,
        margin=dict(t=36, b=16, l=10, r=10),
        coloraxis_showscale=False,
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(size=10)),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(size=10)),
    )
    fig_tahun.update_traces(marker_line_width=0)
    st.plotly_chart(fig_tahun, use_container_width=True, config={'displayModeBar': False})

    # Chart Bulanan
    df_bulan_f = df_f.groupby('month').size().reset_index(name='count')
    bulan_label = ['Jan','Feb','Mar','Apr','Mei','Jun','Jul','Agu','Sep','Okt','Nov','Des']
    df_bulan_f['bulan_label'] = df_bulan_f['month'].apply(lambda x: bulan_label[x-1])
    fig_bulan = px.area(
        df_bulan_f, x='month', y='count',
        labels={'month': 'Bulan', 'count': 'Hotspot'},
        title='Distribusi Hotspot per Bulan',
        color_discrete_sequence=['#FF4500']
    )
    fig_bulan.update_traces(
        fill='tozeroy',
        fillcolor='rgba(255,69,0,0.15)',
        line=dict(color='#FF4500', width=2)
    )
    fig_bulan.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#aaaacc', family='Inter', size=11),
        title=dict(font=dict(size=13, color='#e8e8e8')),
        height=220,
        margin=dict(t=36, b=16, l=10, r=10),
        xaxis=dict(tickvals=list(range(1,13)), ticktext=bulan_label,
                   gridcolor='rgba(255,255,255,0.05)', tickfont=dict(size=10)),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(size=10)),
    )
    st.plotly_chart(fig_bulan, use_container_width=True, config={'displayModeBar': False})


st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)


st.markdown("""
<div class="section-header">
    <div class="section-icon">🤖</div>
    <p class="section-title">Hasil Analisis Kluster DBSCAN</p>
</div>
""", unsafe_allow_html=True)

col_a, col_b = st.columns([3, 2], gap="medium")

with col_a:
    top10 = df_kluster.nlargest(10, 'jumlah_titik').copy()
    top10['cluster'] = top10['cluster'].astype(str)
    top10['nama_daerah'] = top10['nama_daerah'].fillna('Tidak diketahui')
    fig_cluster = px.bar(
        top10, x='nama_daerah', y='jumlah_titik',
        color='avg_frp', color_continuous_scale='YlOrRd',
        title='Top 10 Zona Konsentrasi Karhutla',
        labels={'nama_daerah': 'Daerah', 'jumlah_titik': 'Jumlah Titik', 'avg_frp': 'Avg FRP (MW)'},
        hover_data=['cluster']
    )
    fig_cluster.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#aaaacc', family='Inter', size=11),
        title=dict(font=dict(size=13, color='#e8e8e8')),
        height=320,
        margin=dict(t=36, b=80, l=10, r=10),
        coloraxis_colorbar=dict(tickfont=dict(color='#aaaacc')),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickangle=-35, tickfont=dict(size=9)),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(size=10)),
    )
    fig_cluster.update_traces(marker_line_width=0)
    st.plotly_chart(fig_cluster, use_container_width=True, config={'displayModeBar': False})

with col_b:
    n_kluster  = len(df_kluster)
    n_noise    = (df['cluster'] == -1).sum()
    n_terbesar = df_kluster['jumlah_titik'].max()
    kluster_id = df_kluster.loc[df_kluster['jumlah_titik'].idxmax(), 'cluster']
    nama_terbesar = df_kluster.loc[df_kluster['jumlah_titik'].idxmax(), 'nama_daerah']

    st.markdown(f"""
    <table class="dbscan-table">
        <tr><th>Metrik</th><th>Nilai</th></tr>
        <tr><td>Algoritma</td><td><span class="badge-algo">DBSCAN</span></td></tr>
        <tr><td>Parameter Epsilon</td><td><b style="color:#FF6B35">0.05°</b> (~5.5 km)</td></tr>
        <tr><td>Min Samples</td><td><b style="color:#FF6B35">5 titik</b></td></tr>
        <tr><td>Total Kluster</td><td><b style="color:#ffffff">{n_kluster}</b></td></tr>
        <tr><td>Titik Noise</td><td><b style="color:#ffffff">{n_noise:,}</b></td></tr>
        <tr><td>Kluster Terbesar</td><td><b style="color:#ffffff">{n_terbesar:,} titik</b></td></tr>
        <tr><td>Zona Rawan Utama</td><td><b style="color:#FF6B35">{nama_terbesar}</b></td></tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(255,69,0,0.08);border:1px solid rgba(255,69,0,0.2);
                border-radius:8px;padding:0.7rem 0.9rem;margin-top:0.8rem;
                font-size:0.8rem;color:#aaaacc;line-height:1.5;">
        💡 <b style="color:#FF6B35">Interpretasi:</b> Kluster dengan jumlah titik besar dan FRP tinggi
        menunjukkan zona konsentrasi karhutla yang memerlukan prioritas mitigasi dan pemantauan intensif.
    </div>
    """, unsafe_allow_html=True)


st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)


with st.expander("📄 Eksplorasi Data Mentah (sample 500 baris)"):
    if len(df_f) > 0:
        st.dataframe(
            df_f.sample(min(500, len(df_f)), random_state=42)[[
                'acq_date','latitude','longitude',
                'brightness','frp','confidence',
                'year','month_name','cluster_label','nama_daerah'
            ]].sort_values('acq_date').reset_index(drop=True),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Tidak ada data untuk ditampilkan.")


st.markdown("""
<div class="footer-wrap">
    <span>
        Sumber Data: <b>NASA FIRMS MODIS C6.1</b> &nbsp;|&nbsp;
        Machine Learning: <b>DBSCAN Clustering</b> &nbsp;|&nbsp;
        Visualisasi: <b>Streamlit · Folium · Plotly</b> &nbsp;|&nbsp;
        Wilayah: <b>Provinsi Jambi 2018–2023</b>
    </span>
</div>
""", unsafe_allow_html=True)
