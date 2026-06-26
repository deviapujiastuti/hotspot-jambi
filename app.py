import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

st.set_page_config(
    page_title="🔥 Hotspot Jambi 2018–2023",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0a0a1a 0%, #1a0a0f 50%, #0f0f20 100%);
    color: #e8e8e8;
    overflow-x: hidden;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    padding-top: 1rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

.hero-wrap {
    background: linear-gradient(135deg,
        rgba(255,69,0,0.15) 0%,
        rgba(255,140,0,0.08) 40%,
        rgba(139,0,0,0.08) 100%);
    border: 2px solid rgba(255,69,0,0.3);
    border-radius: 20px;
    padding: 3rem 3rem 2.5rem;
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(255,69,0,0.15),
                inset 0 1px 0 rgba(255,255,255,0.1);
    animation: heroGlow 3s ease-in-out infinite;
}

@keyframes heroGlow {
    0%, 100% { box-shadow: 0 8px 32px rgba(255,69,0,0.15), inset 0 1px 0 rgba(255,255,255,0.1); }
    50% { box-shadow: 0 12px 40px rgba(255,69,0,0.25), inset 0 1px 0 rgba(255,255,255,0.15); }
}

.hero-wrap::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(255,69,0,0.12) 0%, transparent 70%);
    pointer-events: none;
    animation: float 6s ease-in-out infinite;
}

.hero-wrap::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: -5%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(139,0,0,0.08) 0%, transparent 70%);
    pointer-events: none;
    animation: float 8s ease-in-out infinite reverse;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}

.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(255,69,0,0.2), rgba(255,140,0,0.1));
    border: 1px solid rgba(255,69,0,0.5);
    color: #FF6B35;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 6px 16px;
    border-radius: 25px;
    margin-bottom: 1rem;
    box-shadow: 0 4px 15px rgba(255,69,0,0.2);
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.5rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.2;
    margin: 0.5rem 0 1rem;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #ffffff 0%, #FFB366 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-title span {
    color: #FF4500;
    text-shadow: 0 0 20px rgba(255,69,0,0.4);
}

.hero-sub {
    font-size: 0.95rem;
    color: #b8b8cc;
    font-weight: 400;
    margin: 0;
    line-height: 1.6;
}

.hero-sub b {
    color: #FFB366;
    font-weight: 600;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 2rem;
}

.metric-card {
    background: linear-gradient(135deg,
        rgba(255,69,0,0.08) 0%,
        rgba(255,140,0,0.04) 100%);
    border: 2px solid rgba(255,69,0,0.2);
    border-radius: 16px;
    padding: 1.5rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
}

.metric-card:hover {
    border-color: rgba(255,69,0,0.5);
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(255,69,0,0.25);
}

.metric-card::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(255,69,0,0.3), transparent 70%);
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.3s;
}

.metric-card:hover::before {
    opacity: 1;
}

.metric-card::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, #FF4500, #FFB366, transparent);
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.metric-card:hover::after {
    transform: scaleX(1);
}

.metric-icon {
    font-size: 1.8rem;
    margin-bottom: 0.8rem;
    animation: bounce 2s ease-in-out infinite;
}

.metric-card:nth-child(2) .metric-icon { animation-delay: 0.1s; }
.metric-card:nth-child(3) .metric-icon { animation-delay: 0.2s; }
.metric-card:nth-child(4) .metric-icon { animation-delay: 0.3s; }

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}

.metric-val {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #FFB366, #FF6B35);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin-bottom: 0.4rem;
}

.metric-label {
    font-size: 0.8rem;
    color: #8a8a9a;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
}

.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid rgba(255,69,0,0.2);
    position: relative;
}

.section-header::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    height: 2px;
    width: 60px;
    background: linear-gradient(90deg, #FF4500, #FFB366);
    animation: slideRight 0.6s ease-out;
}

@keyframes slideRight {
    from { width: 0; }
    to { width: 60px; }
}

.section-icon {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, rgba(255,69,0,0.2), rgba(255,140,0,0.1));
    border: 2px solid rgba(255,69,0,0.3);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    box-shadow: 0 4px 15px rgba(255,69,0,0.15);
}

.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
    letter-spacing: -0.01em;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d1a 0%, #0a0a12 100%) !important;
    border-right: 2px solid rgba(255,69,0,0.15) !important;
    width: 300px !important;
    z-index: 9999 !important;
}

[data-testid="stAppViewContainer"] {
        margin-left: 300px !important;
}
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown p {
    color: #e8e8e8 !important;
}

.sidebar-brand {
    background: linear-gradient(135deg, rgba(255,69,0,0.2), rgba(255,140,0,0.1));
    border: 2px solid rgba(255,69,0,0.3);
    border-radius: 14px;
    padding: 1.2rem 1.3rem;
    margin-bottom: 1.5rem;
    text-align: center;
    box-shadow: 0 8px 25px rgba(255,69,0,0.15);
    position: relative;
    overflow: hidden;
}

.sidebar-brand::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(255,69,0,0.2), transparent 70%);
    animation: spin 4s linear infinite;
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.sidebar-brand-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    font-weight: 800;
    background: linear-gradient(135deg, #FF6B35, #FFB366);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 0.05em;
    position: relative;
    z-index: 1;
}

.sidebar-brand-sub {
    font-size: 0.75rem;
    color: #8a8a9a;
    margin-top: 4px;
    position: relative;
    z-index: 1;
    font-weight: 500;
}

[data-testid="stSidebar"] .stSelectbox,
[data-testid="stSidebar"] .stMultiSelect,
[data-testid="stSidebar"] .stSlider {
    margin-bottom: 1rem;
}

[data-testid="stSidebar"] .stMarkdown {
    margin-bottom: 0.5rem;
}

[data-testid="stSidebar"] .stMarkdown h2 {
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    color: #FFB366 !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.5rem !important;
}

.info-box {
    background: linear-gradient(135deg,
        rgba(255,69,0,0.08) 0%,
        rgba(255,140,0,0.04) 100%);
    border: 2px solid rgba(255,69,0,0.2);
    border-left: 4px solid #FF4500;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    font-size: 0.85rem;
    color: #b8b8cc;
    line-height: 1.6;
    margin-top: 1rem;
    box-shadow: 0 4px 15px rgba(255,69,0,0.1);
}

.info-box b {
    color: #FFB366;
    font-weight: 700;
}

.map-container {
    background: linear-gradient(135deg,
        rgba(255,69,0,0.05) 0%,
        rgba(0,0,0,0.3) 100%);
    border: 2px solid rgba(255,69,0,0.15);
    border-radius: 16px;
    padding: 1.2rem;
    height: 100%;
    overflow: hidden;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
}

.js-plotly-plot {
    border-radius: 12px !important;
    overflow: hidden !important;
}

.custom-divider {
    height: 2px;
    background: linear-gradient(90deg,
        transparent,
        rgba(255,69,0,0.3),
        transparent);
    margin: 2.5rem 0;
}

.dbscan-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
    margin-top: 0.5rem;
}

.dbscan-table th {
    background: linear-gradient(90deg,
        rgba(255,69,0,0.15) 0%,
        rgba(255,140,0,0.08) 100%);
    color: #FFB366;
    font-weight: 700;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 0.8rem 1rem;
    border-bottom: 2px solid rgba(255,69,0,0.2);
    text-align: left;
}

.dbscan-table td {
    padding: 0.8rem 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    color: #d8d8e8;
}

.dbscan-table tr:hover td {
    background: rgba(255,69,0,0.05);
    transition: background 0.2s;
}

.badge-algo {
    display: inline-block;
    background: linear-gradient(135deg, rgba(255,69,0,0.2), rgba(255,140,0,0.1));
    border: 1px solid rgba(255,69,0,0.3);
    color: #FF6B35;
    font-size: 0.75rem;
    padding: 4px 10px;
    border-radius: 6px;
    font-weight: 700;
    letter-spacing: 0.05em;
}

.footer-wrap {
    text-align: center;
    padding: 1.5rem;
    margin-top: 3rem;
    border-top: 2px solid rgba(255,69,0,0.15);
    background: rgba(255,69,0,0.02);
    border-radius: 12px;
}

.footer-wrap span {
    font-size: 0.8rem;
    color: #7a7a8a;
    letter-spacing: 0.05em;
    line-height: 1.6;
}

.footer-wrap b {
    color: #FFB366;
    font-weight: 700;
}

.stat-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 12px;
    margin-top: 1.5rem;
}

.stat-item {
    background: linear-gradient(135deg,
        rgba(255,69,0,0.08) 0%,
        rgba(255,140,0,0.04) 100%);
    border: 2px solid rgba(255,69,0,0.15);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    text-align: center;
    transition: all 0.3s;
}

.stat-item:hover {
    border-color: rgba(255,69,0,0.3);
    transform: translateY(-3px);
}

.stat-num {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #FF6B35, #FFB366);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.stat-desc {
    font-size: 0.75rem;
    color: #8a8a9a;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.4rem;
    font-weight: 600;
}

.streamlit-expanderHeader {
    background: linear-gradient(135deg,
        rgba(255,69,0,0.08) 0%,
        rgba(255,140,0,0.04) 100%) !important;
    border: 1px solid rgba(255,69,0,0.15) !important;
    border-radius: 10px !important;
}

.streamlit-expanderHeader:hover {
    border-color: rgba(255,69,0,0.3) !important;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.loading-pulse {
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@media (max-width: 768px) {
    .hero-title { font-size: 1.8rem; }
    .metric-grid { grid-template-columns: repeat(2, 1fr); }
    .section-header { margin-bottom: 1rem; }
}

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
        <div class="sidebar-brand-sub">🛰️ Spasio-Temporal Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🗓️ Rentang Waktu")
    tahun_list  = sorted(df['year'].unique())
    tahun_pilih = st.multiselect(
        "Pilih Tahun",
        options=tahun_list,
        default=tahun_list,
        label_visibility="collapsed"
    )

    st.markdown("### 📅 Bulan")
    bulan_nama  = ['January','February','March','April','May','June',
                   'July','August','September','October','November','December']
    bulan_pilih = st.multiselect(
        "Pilih Bulan",
        options=bulan_nama,
        default=bulan_nama,
        label_visibility="collapsed"
    )

    st.markdown("### 🗺️ Mode Peta")
    mode_peta = st.selectbox(
        "Pilih Visualisasi Peta",
        ["🔥 Heatmap", "📍 Marker Kluster", "🎯 Kluster DBSCAN"],
        label_visibility="collapsed"
    )

    st.markdown("### 🎯 Confidence Level")
    min_conf = st.slider(
        "Minimum Confidence (%)",
        30, 100, 50,
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("""
    <div class="info-box">
        <b>📡 Data Source:</b> NASA FIRMS MODIS C6.1<br><br>
        <b>🤖 Metode:</b> DBSCAN Clustering<br><br>
        <b>📍 Wilayah:</b> Provinsi Jambi<br><br>
        <b>📆 Periode:</b> 2018 – 2023
    </div>
    """, unsafe_allow_html=True)

df_f = df[
    (df['year'].isin(tahun_pilih)) &
    (df['month_name'].isin(bulan_pilih)) &
    (df['confidence'] >= min_conf)
]


st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">🛰️ NASA FIRMS · MODIS C6.1 · Provinsi Jambi</div>
    <div class="hero-title">Pemetaan <span>Spasio-Temporal</span><br>Hotspot Karhutla Jambi</div>
    <p class="hero-sub">
        Analisis pola sebaran dan konsentrasi titik panas kebakaran hutan dan lahan di Provinsi Jambi
        periode <b>2018–2023</b> menggunakan teknologi machine learning <b>DBSCAN</b> dan visualisasi
        interaktif real-time.
    </p>
</div>
""", unsafe_allow_html=True)

if len(df_f) > 0:
    avg_br  = f"{df_f['brightness'].mean():.1f} K"
    avg_frp = f"{df_f['frp'].mean():.1f} MW"
    pct_year = f"{(len(df_f) / len(df) * 100):.1f}%"
    max_day = df_f.groupby('acq_date').size().max()
else:
    avg_br  = "—"
    avg_frp = "—"
    pct_year = "—"
    max_day = "—"

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
        <div class="metric-label">Avg FRP Power</div>
    </div>
    <div class="metric-card">
        <div class="metric-icon">📊</div>
        <div class="metric-val">{pct_year}</div>
        <div class="metric-label">Persentase Data</div>
    </div>
</div>
""", unsafe_allow_html=True)

col_map, col_chart = st.columns([3, 2], gap="medium")

with col_map:
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🗺️</div>
        <p class="section-title">Peta Sebaran Hotspot</p>
    </div>
    """, unsafe_allow_html=True)

    if len(df_f) == 0:
        st.warning("⚠️ **Tidak ada data** untuk filter yang dipilih. Coba ubah filter di sidebar.")
    else:
        m = folium.Map(
            location=[-1.5, 102.8],
            zoom_start=7,
            tiles="CartoDB dark_matter"
        )

        # Bounding Box Jambi
        folium.Rectangle(
            bounds=[[-3.0, 101.5], [0.0, 104.7]],
            color="#FF4500",
            fill=False,
            weight=2,
            dash_array="8 5",
            popup="Bounding Box Provinsi Jambi",
            tooltip="Batas Administratif Jambi"
        ).add_to(m)

        if mode_peta == "🔥 Heatmap":
            heat_data = df_f[['latitude', 'longitude', 'frp']].values.tolist()
            HeatMap(
                heat_data,
                min_opacity=0.3,
                max_zoom=10,
                radius=15,
                blur=18,
                gradient={0.2:'#0066ff', 0.4:'#00ff00', 0.6:'#ffff00', 0.8:'#ff6600', 1.0:'#ff0000'}
            ).add_to(m)

            legend_html = """
            <div style="position:fixed;bottom:20px;left:20px;z-index:1000;
                        background:rgba(10,10,20,0.95);padding:14px 18px;
                        border-radius:12px;color:white;font-size:12px;
                        border:2px solid rgba(255,69,0,0.3);font-family:Poppins,sans-serif;
                        box-shadow: 0 8px 25px rgba(255,69,0,0.2);">
                <div style="color:#FF6B35;font-weight:700;letter-spacing:.05em;margin-bottom:10px;">
                    🔥 INTENSITAS FRP
                </div>
                <div style="font-size:11px;">
                    <div style="margin-bottom:6px;">
                        <span style="color:#0066ff;font-weight:600;">■</span>&nbsp;Rendah (Dingin)
                    </div>
                    <div style="margin-bottom:6px;">
                        <span style="color:#00ff00;font-weight:600;">■</span>&nbsp;Sedang (Hangat)
                    </div>
                    <div style="margin-bottom:6px;">
                        <span style="color:#ffff00;font-weight:600;">■</span>&nbsp;Tinggi (Panas)
                    </div>
                    <div style="margin-bottom:6px;">
                        <span style="color:#ff6600;font-weight:600;">■</span>&nbsp;Sangat Tinggi
                    </div>
                    <div>
                        <span style="color:#ff0000;font-weight:600;">■</span>&nbsp;Ekstrem (Sangat Panas)
                    </div>
                </div>
            </div>"""
            m.get_root().html.add_child(folium.Element(legend_html))

        elif mode_peta == "📍 Marker Kluster":
            mc = MarkerCluster(name="Hotspot Cluster", options={'maxClusterRadius': 50}).add_to(m)
            sample = df_f.sample(min(2000, len(df_f)), random_state=42)

            for _, row in sample.iterrows():
                folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=5,
                    color='#FF4500',
                    fill=True,
                    fill_color='#FF6B35',
                    fill_opacity=0.8,
                    weight=1.5,
                    popup=folium.Popup(
                        f"""<div style='font-family:Poppins,sans-serif;font-size:12px;
                                        min-width:200px;color:#333;'>
                            <div style='background:linear-gradient(135deg,#FF4500,#FFB366);
                                        color:white;padding:8px;border-radius:6px;
                                        font-weight:700;margin-bottom:8px;'>
                                📍 {row['nama_daerah']}
                            </div>
                            <table style='width:100%;border-collapse:collapse;font-size:11px;'>
                                <tr style='border-bottom:1px solid #eee;'>
                                    <td style='padding:4px;font-weight:600;'>Kluster:</td>
                                    <td style='padding:4px;color:#FF4500;'>{row['cluster_label']}</td>
                                </tr>
                                <tr style='border-bottom:1px solid #eee;'>
                                    <td style='padding:4px;font-weight:600;'>Tanggal:</td>
                                    <td style='padding:4px;'>{row['acq_date'].date()}</td>
                                </tr>
                                <tr style='border-bottom:1px solid #eee;'>
                                    <td style='padding:4px;font-weight:600;'>Brightness:</td>
                                    <td style='padding:4px;'>{row['brightness']:.1f} K</td>
                                </tr>
                                <tr style='border-bottom:1px solid #eee;'>
                                    <td style='padding:4px;font-weight:600;'>FRP:</td>
                                    <td style='padding:4px;color:#FF6B35;font-weight:600;'>{row['frp']:.2f} MW</td>
                                </tr>
                                <tr>
                                    <td style='padding:4px;font-weight:600;'>Confidence:</td>
                                    <td style='padding:4px;'>{row['confidence']}%</td>
                                </tr>
                            </table>
                        </div>""",
                        max_width=240
                    )
                ).add_to(mc)

        elif mode_peta == "🎯 Kluster DBSCAN":
            clr = px.colors.qualitative.Set3
            top_clusters = df_f[df_f['cluster'] >= 0]['cluster'].value_counts().head(12).index.tolist()

            for _, row in df_f.iterrows():
                if row['cluster'] == -1:
                    color, label = '#555566', 'Noise/Outlier'
                    radius = 2.5
                elif row['cluster'] in top_clusters:
                    color = clr[top_clusters.index(row['cluster']) % len(clr)]
                    label = f"Kluster {row['cluster']}"
                    radius = 4
                else:
                    color, label = '#FFAA00', f"Kluster {row['cluster']}"
                    radius = 3

                folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=radius,
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.7,
                    weight=1,
                    popup=folium.Popup(
                        f"""<div style='font-family:Poppins,sans-serif;font-size:12px;
                                        min-width:200px;color:#333;'>
                            <div style='background:linear-gradient(135deg,{color},#FFB366);
                                        color:white;padding:8px;border-radius:6px;
                                        font-weight:700;margin-bottom:8px;'>
                                📍 {row['nama_daerah']}
                            </div>
                            <table style='width:100%;border-collapse:collapse;font-size:11px;'>
                                <tr style='border-bottom:1px solid #eee;'>
                                    <td style='padding:4px;font-weight:600;'>Status:</td>
                                    <td style='padding:4px;'>{label}</td>
                                </tr>
                                <tr style='border-bottom:1px solid #eee;'>
                                    <td style='padding:4px;font-weight:600;'>Tanggal:</td>
                                    <td style='padding:4px;'>{row['acq_date'].date()}</td>
                                </tr>
                                <tr style='border-bottom:1px solid #eee;'>
                                    <td style='padding:4px;font-weight:600;'>FRP:</td>
                                    <td style='padding:4px;color:#FF6B35;font-weight:600;'>{row['frp']:.2f} MW</td>
                                </tr>
                                <tr>
                                    <td style='padding:4px;font-weight:600;'>Confidence:</td>
                                    <td style='padding:4px;'>{row['confidence']}%</td>
                                </tr>
                            </table>
                        </div>""",
                        max_width=220
                    )
                ).add_to(m)

            legend_html = """
            <div style="position:fixed;bottom:20px;left:20px;z-index:1000;
                        background:rgba(10,10,20,0.95);padding:14px 18px;
                        border-radius:12px;color:white;font-size:12px;
                        border:2px solid rgba(255,69,0,0.3);font-family:Poppins,sans-serif;
                        box-shadow: 0 8px 25px rgba(255,69,0,0.2);">
                <div style="color:#FF6B35;font-weight:700;letter-spacing:.05em;margin-bottom:10px;">
                    🎯 KLUSTER DBSCAN
                </div>
                <div style="font-size:11px;">
                    <div style="margin-bottom:6px;">
                        <span style="color:#e41a1c;font-weight:600;">●</span>&nbsp;Top 12 Kluster
                    </div>
                    <div style="margin-bottom:6px;">
                        <span style="color:#ffaa00;font-weight:600;">●</span>&nbsp;Kluster Lainnya
                    </div>
                    <div>
                        <span style="color:#555566;font-weight:600;">●</span>&nbsp;Noise/Outlier
                    </div>
                </div>
            </div>"""
            m.get_root().html.add_child(folium.Element(legend_html))

        folium.LayerControl(position='topright').add_to(m)
        st_folium(m, width=None, height=500, use_container_width=True)

with col_chart:
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">📊</div>
        <p class="section-title">Analisis Temporal</p>
    </div>
    """, unsafe_allow_html=True)

    # Chart Tahunan
    if len(df_f) > 0:
        df_tahun_f = df_f.groupby('year').size().reset_index(name='count')

        fig_tahun = px.bar(
            df_tahun_f, x='year', y='count',
            color='count',
            color_continuous_scale=[[0, '#0066ff'], [0.25, '#00ff00'], [0.5, '#ffff00'],
                                    [0.75, '#ff6600'], [1, '#ff0000']],
            labels={'year': 'Tahun', 'count': 'Hotspot'},
            title='📈 Hotspot per Tahun'
        )

        fig_tahun.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#9a9aaa', family='Poppins', size=11),
            title=dict(font=dict(size=13, color='#e8e8e8'), x=0.05),
            showlegend=False,
            height=240,
            margin=dict(t=40, b=20, l=10, r=10),
            coloraxis_showscale=False,
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.05)',
                tickfont=dict(size=10),
                showgrid=True
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.05)',
                tickfont=dict(size=10),
                showgrid=True
            ),
        )

        fig_tahun.update_traces(
            marker=dict(line=dict(width=0), cornerradius=6),
            hovertemplate='<b>%{x}</b><br>Hotspot: %{y:,.0f}<extra></extra>'
        )

        st.plotly_chart(fig_tahun, use_container_width=True, config={
            'displayModeBar': False,
            'responsive': True
        })

        # Chart Bulanan
        df_bulan_f = df_f.groupby('month').size().reset_index(name='count')
        bulan_label = ['Jan','Feb','Mar','Apr','Mei','Jun','Jul','Agu','Sep','Okt','Nov','Des']
        df_bulan_f['bulan_label'] = df_bulan_f['month'].apply(lambda x: bulan_label[x-1])

        fig_bulan = px.area(
            df_bulan_f, x='month', y='count',
            labels={'month': 'Bulan', 'count': 'Hotspot'},
            title='📅 Distribusi per Bulan',
            color_discrete_sequence=['#FF4500']
        )

        fig_bulan.update_traces(
            fill='tozeroy',
            fillcolor='rgba(255,69,0,0.25)',
            line=dict(color='#FF4500', width=3),
            hovertemplate='<b>%{x|%b}</b><br>Hotspot: %{y:,.0f}<extra></extra>'
        )

        fig_bulan.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#9a9aaa', family='Poppins', size=11),
            title=dict(font=dict(size=13, color='#e8e8e8'), x=0.05),
            height=240,
            margin=dict(t=40, b=20, l=10, r=10),
            xaxis=dict(
                tickvals=list(range(1,13)),
                ticktext=bulan_label,
                gridcolor='rgba(255,255,255,0.05)',
                tickfont=dict(size=10),
                showgrid=True
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.05)',
                tickfont=dict(size=10),
                showgrid=True
            ),
        )

        st.plotly_chart(fig_bulan, use_container_width=True, config={
            'displayModeBar': False,
            'responsive': True
        })
    else:
        st.info("📊 Tidak ada data temporal untuk ditampilkan")

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="section-header">
    <div class="section-icon">🤖</div>
    <p class="section-title">Hasil Analisis Kluster DBSCAN</p>
</div>
""", unsafe_allow_html=True)

col_a, col_b = st.columns([3, 2], gap="medium")

with col_a:
    if len(df_f) > 0 and len(df_kluster) > 0:
        top10 = df_kluster.nlargest(10, 'jumlah_titik').copy()
        top10['cluster'] = top10['cluster'].astype(str)
        top10['nama_daerah'] = top10['nama_daerah'].fillna('Tidak diketahui')

        fig_cluster = px.bar(
            top10, x='nama_daerah', y='jumlah_titik',
            color='avg_frp',
            color_continuous_scale=[[0, '#0066ff'], [0.33, '#ffff00'], [0.66, '#ff6600'], [1, '#ff0000']],
            title='🔥 Top 10 Zona Konsentrasi Karhutla',
            labels={'nama_daerah': 'Daerah', 'jumlah_titik': 'Jumlah Titik', 'avg_frp': 'Avg FRP (MW)'},
            hover_data={'cluster': True, 'nama_daerah': False}
        )

        fig_cluster.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#9a9aaa', family='Poppins', size=11),
            title=dict(font=dict(size=13, color='#e8e8e8'), x=0.05),
            height=340,
            margin=dict(t=40, b=100, l=10, r=10),
            coloraxis_colorbar=dict(
                title=dict(text='Avg FRP', font=dict(color='#9a9aaa')),
                tickfont=dict(color='#9a9aaa')
            ),
            xaxis=dict(
                tickangle=-40,
                tickfont=dict(size=9),
                gridcolor='rgba(255,255,255,0.05)',
                showgrid=False
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.05)',
                tickfont=dict(size=10),
                showgrid=True
            ),
        )

        fig_cluster.update_traces(
            marker=dict(line=dict(width=0), cornerradius=6),
            hovertemplate='<b>%{x}</b><br>Titik: %{y:,.0f}<br>Avg FRP: %{marker.color:.2f} MW<extra></extra>'
        )

        st.plotly_chart(fig_cluster, use_container_width=True, config={
            'displayModeBar': False,
            'responsive': True
        })
    else:
        st.info("📊 Tidak ada data kluster untuk ditampilkan")

with col_b:
    if len(df_kluster) > 0:
        n_kluster  = len(df_kluster)
        n_noise    = (df['cluster'] == -1).sum()
        n_terbesar = df_kluster['jumlah_titik'].max()
        kluster_id = df_kluster.loc[df_kluster['jumlah_titik'].idxmax(), 'cluster']
        nama_terbesar = df_kluster.loc[df_kluster['jumlah_titik'].idxmax(), 'nama_daerah']
        avg_frp_terbesar = df_kluster.loc[df_kluster['jumlah_titik'].idxmax(), 'avg_frp']

        st.markdown(f"""
        <table class="dbscan-table">
            <tr>
                <th style="width:45%;">Metrik</th>
                <th style="width:55%;">Nilai</th>
            </tr>
            <tr>
                <td>🤖 Algoritma</td>
                <td><span class="badge-algo">DBSCAN v2.0</span></td>
            </tr>
            <tr>
                <td>📏 Parameter Epsilon</td>
                <td><b style="color:#FF6B35;">0.05°</b> (~5.5 km)</td>
            </tr>
            <tr>
                <td>🎯 Min Samples</td>
                <td><b style="color:#FF6B35;">5 titik</b></td>
            </tr>
            <tr>
                <td>📊 Total Kluster</td>
                <td><b style="color:#FFB366;">{n_kluster}</b></td>
            </tr>
            <tr>
                <td>🔸 Titik Noise</td>
                <td><b style="color:#ffffff;">{n_noise:,}</b></td>
            </tr>
            <tr>
                <td>🔥 Kluster Terbesar</td>
                <td><b style="color:#FF6B35;">{n_terbesar:,}</b> titik</td>
            </tr>
            <tr>
                <td>📍 Zona Rawan Utama</td>
                <td><b style="color:#FFB366;">{nama_terbesar}</b></td>
            </tr>
            <tr>
                <td>⚡ Avg FRP Utama</td>
                <td><b style="color:#FF6B35;">{avg_frp_terbesar:.2f}</b> MW</td>
            </tr>
        </table>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:linear-gradient(135deg,
                    rgba(255,69,0,0.12) 0%,
                    rgba(255,140,0,0.06) 100%);
                    border:2px solid rgba(255,69,0,0.2);
                    border-left:4px solid #FF4500;
                    border-radius:10px;
                    padding:1rem 1.2rem;
                    margin-top:1rem;
                    font-size:0.85rem;
                    color:#b8b8cc;
                    line-height:1.6;">
            <b style="color:#FF6B35;">💡 Interpretasi:</b><br>
            Kluster dengan jumlah titik besar dan FRP tinggi menunjukkan zona konsentrasi
            karhutla dengan risiko tinggi. Prioritaskan mitigasi dan pemantauan intensif di area-area tersebut.
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

with st.expander("📄 **Eksplorasi Data Mentah** (sample 500 baris terbaru)", expanded=False):
    if len(df_f) > 0:
        sample_data = df_f.sample(min(500, len(df_f)), random_state=42)[[
            'acq_date', 'latitude', 'longitude',
            'brightness', 'frp', 'confidence',
            'year', 'month_name', 'cluster_label', 'nama_daerah'
        ]].sort_values('acq_date', ascending=False).reset_index(drop=True)

        # Styling dataframe
        st.dataframe(
            sample_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "acq_date": st.column_config.DateColumn("Tanggal", format="DD/MM/YYYY"),
                "latitude": st.column_config.NumberColumn("Latitude", format="%.4f"),
                "longitude": st.column_config.NumberColumn("Longitude", format="%.4f"),
                "brightness": st.column_config.NumberColumn("Brightness (K)", format="%.1f"),
                "frp": st.column_config.NumberColumn("FRP (MW)", format="%.2f"),
                "confidence": st.column_config.NumberColumn("Confidence (%)", format="%d"),
                "year": st.column_config.NumberColumn("Tahun"),
                "month_name": st.column_config.TextColumn("Bulan"),
                "cluster_label": st.column_config.TextColumn("Kluster"),
                "nama_daerah": st.column_config.TextColumn("Daerah"),
            }
        )
    else:
        st.info("📊 Tidak ada data untuk ditampilkan dengan filter yang dipilih")

st.markdown("""
<div class="footer-wrap">
    <span>
        🛰️ <b>Sumber Data:</b> NASA FIRMS MODIS C6.1 &nbsp;|&nbsp;
        🤖 <b>Machine Learning:</b> DBSCAN Clustering &nbsp;|&nbsp;
        📊 <b>Visualisasi:</b> Streamlit · Folium · Plotly &nbsp;|&nbsp;
        📍 <b>Area:</b> Provinsi Jambi (2018–2023)
    </span>
</div>
""", unsafe_allow_html=True)
