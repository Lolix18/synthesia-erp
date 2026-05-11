import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from supabase import create_client

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="SYNTHESIA ERP", layout="wide", page_icon="🕹️")

# --- 2. CONEXIÓN SILENCIOSA A SUPABASE ---
URL = "https://yalomimyjgaofjsxxtff.supabase.co"
KEY = "sb_publishable_am9lY29ubm9yQGdtYWlsLmNvbToxNzMxOTkyNTQ3Nzg5"

try:
    supabase = create_client(URL, KEY)
    res = supabase.table('inventario').select("*").execute()
    df_nube = pd.DataFrame(res.data)
    stock_real = df_nube['stock'].sum() if not df_nube.empty else "2,850"
except:
    stock_real = "2,850" # Si falla el internet, muestra el de la imagen

# --- 3. CSS AVANZADO (IDÉNTICO A TU IMAGEN) ---
st.markdown("""
    <style>
    /* Fondo principal y ocultar márgenes */
    .stApp { background-color: #12161F !important; }
    .block-container { padding-top: 2rem !important; padding-bottom: 0rem !important; max-width: 100% !important; }
    
    /* Sidebar oscuro */
    [data-testid="stSidebar"] {
        background-color: #1A202C !important;
        border-right: 1px solid #2D3748 !important;
    }
    
    /* Magia: Ocultar los círculos del menú y darle estilo texto */
    div[role="radiogroup"] > div > label > div:first-of-type { display: none !important; }
    div[role="radiogroup"] > div > label p {
        font-size: 15px !important;
        font-weight: 500 !important;
        color: #A0AEC0 !important;
        margin-bottom: 8px;
        transition: all 0.3s;
    }
    div[role="radiogroup"] > div > label:hover p { color: #FFFFFF !important; }
    div[role="radiogroup"] > div[data-checked="true"] p {
        color: #00FBFF !important;
        font-weight: 700 !important;
    }

    /* Tarjetas del Dashboard (Cards) */
    .dashboard-card {
        background-color: #1E2532;
        border-radius: 8px;
        padding: 20px;
        border: 1px solid #2D3748;
        height: 100%;
    }
    .card-title { color: #A0AEC0; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
    .card-value { font-size: 28px; font-weight: 700; color: #FFFFFF; margin: 0; line-height: 1.2; }
    
    /* Tablas inferiores */
    .custom-table { width: 100%; border-collapse: collapse; color: #FFFFFF; font-size: 13px; }
    .custom-table th { color: #A0AEC0; font-weight: 600; text-align: left; padding-bottom: 15px; border-bottom: 1px solid #2D3748; font-size: 11px; text-transform: uppercase; }
    .custom-table td { padding: 12px 0; border-bottom: 1px solid #2D3748; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color: white; font-family: sans-serif;'>SYNTHESIA <span style='color: #00FBFF;'>ERP</span></h2><br>", unsafe_allow_html=True)
    menu = st.radio("Navegación", 
        ["▦ DASHBOARD", "📦 INVENTARIO", "↑ SALIDAS", "↓ ENTRADAS", "🛒 VENTAS", "👥 CLIENTES", "📈 ANÁLISIS", "⚙️ CONFIGURACIÓN"], 
        label_visibility="collapsed"
    )

# --- 5. PANTALLA PRINCIPAL (DASHBOARD) ---
if menu == "▦ DASHBOARD":
    
    # KPIs Superiores
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class="dashboard-card"><div class="card-title">RESUMEN VENTAS (S/)</div><div class="card-value">S/ 25,680</div><div style="color: #00FBFF; margin-top: 10px; font-size: 13px;">📈 Tendencia alcista</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="dashboard-card"><div class="card-title">STOCK ACTUAL</div><div class="card-value">{stock_real} <span style="font-size: 14px; color: #A0AEC0;">units</span></div><div style="width: 100%; background-color: #2D3748; height: 6px; border-radius: 3px; margin-top: 15px;"><div style="width: 75%; background-color: #00FBFF; height: 6px; border-radius: 3px;"></div></div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="dashboard-card"><div class="card-title">NUEVOS CLIENTES</div><div class="card-value">145</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class="dashboard-card"><div class="card-title">ÓRDENES PROCESADAS</div><div class="card-value">789</div></div>""", unsafe_allow_html=True)

    st.write("") # Espacio

    # Gráficos Centrales (Plotly)
    c_chart1, c_chart2, c_chart3 = st.columns([2, 1, 1])
    
    with c_chart1:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">SALIDAS VS ENTRADAS (ÚLTIMOS 30 DÍAS)</div>', unsafe_allow_html=True)
        meses = ['19 Jun', '15 Jun', '20 Jun', '26 Jun', '23 Jun', '01 Jun', '13 Nov', '15 Nov', '20 Nov', '25 Nov']
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(x=meses, y=[280, 310, 380, 350, 420, 250, 320, 360, 410, 330], name='Salidas', marker_color='#00FBFF'))
        fig1.add_trace(go.Bar(x=meses, y=[200, 220, 260, 240, 300, 180, 230, 270, 310, 240], name='Entradas', marker_color='#D53F8C'))
        fig1.update_layout(barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#A0AEC0', size=10), margin=dict(l=0, r=0, t=10, b=0), height=250, legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5))
        fig1.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#2D3748')
        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    with c_chart2:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">TOP 5 PRODUCTOS</div>', unsafe_allow_html=True)
        fig2 = go.Figure(data=[go.Pie(labels=['Game Stick Pro', 'R36S', 'Controles', 'Fundas', 'Cables'], values=[37.6, 18.7, 11.2, 6.67, 25.8], hole=.6, marker_colors=['#00FBFF', '#3182CE', '#D53F8C', '#805AD5', '#2B6CB0'])])
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#A0AEC0', size=10), margin=dict(l=0, r=0, t=10, b=0), height=250, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    with c_chart3:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">MÉTODOS DE PAGO</div>', unsafe_allow_html=True)
        fig3 = go.Figure(data=[go.Pie(labels=['Efectivo', 'Transferencia', 'Tarjeta'], values=[38.3, 25.2, 36.4], hole=.6, marker_colors=['#00FBFF', '#D53F8C', '#3182CE'])])
        fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#A0AEC0', size=10), margin=dict(l=0, r=0, t=10, b=0), height=250, legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5))
        st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("") # Espacio

    # Tablas Inferiores
    c_table1, c_table2 = st.columns(2)
    with c_table1:
        st.markdown("""
            <div class="dashboard-card">
                <div class="card-title" style="color: #F6AD55;">⚠️ STOCK CRÍTICO & ALERTAS</div>
                <table class="custom-table">
                    <tr><th>PRODUCTO</th><th>SKU</th><th>CURRENT STOCK</th><th>STATUS</th></tr>
                    <tr><td>🕹️ R36S BLACK</td><td style="color: #A0AEC0;">SKU-001</td><td>3 Units</td><td style="color: #FC8181;">ALERTA</td></tr>
                    <tr><td>🎮 R36S PORTABLE</td><td style="color: #A0AEC0;">SKU-002</td><td>4 Units</td><td style="color: #FC8181;">ALERTA</td></tr>
                </table>
            </div>
        """, unsafe_allow_html=True)

    with c_table2:
        st.markdown("""
            <div class="dashboard-card">
                <div class="card-title">CLIENTES RECIENTES</div>
                <table class="custom-table">
                    <tr><th>CUSTOMER</th><th>INTERACCIÓN</th><th>FECHA</th><th>STATUS</th></tr>
                    <tr><td>👤 Amara Rihon</td><td style="color: #A0AEC0;">Interacción</td><td>29/05/2026</td><td style="color: #A0AEC0;">Aterato</td></tr>
                    <tr><td>👤 Marbel Ramen</td><td style="color: #A0AEC0;">Interacción</td><td>23/05/2026</td><td style="color: #A0AEC0;">Aterato</td></tr>
                </table>
            </div>
        """, unsafe_allow_html=True)

else:
    st.markdown(f"<h2 style='color: #00FBFF; margin-top: 20px;'>Módulo de {menu}</h2>", unsafe_allow_html=True)
    st.markdown('<div class="dashboard-card">Este módulo mantendrá el diseño oscuro cuando agreguemos los formularios.</div>', unsafe_allow_html=True)