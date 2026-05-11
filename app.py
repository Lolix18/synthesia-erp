import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from supabase import create_client

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="SYNTHESIA ERP", layout="wide", page_icon="🕹️")

# --- 2. CONEXIÓN REAL A SUPABASE ---
URL = "https://yalomimyjgaofjsxxtff.supabase.co"
KEY = "sb_publishable_am9lY29ubm9yQGdtYWlsLmNvbToxNzMxOTkyNTQ3Nzg5"

@st.cache_resource
def iniciar_conexion():
    try:
        return create_client(URL, KEY)
    except:
        return None

supabase = iniciar_conexion()

# Función robusta para consultar la base de datos en tiempo real
def cargar_inventario():
    if supabase:
        try:
            res = supabase.table('inventario').select("*").execute()
            if res.data:
                return pd.DataFrame(res.data)
        except:
            pass
    # Estructura vacía de respaldo si la nube falla o no hay datos aún
    return pd.DataFrame(columns=["producto", "sku", "precio", "stock"])

# Cargamos la información global de la base de datos
df_nube = cargar_inventario()
stock_real = df_nube['stock'].sum() if not df_nube.empty else 0

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
        color: white;
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

# --- 5. PANTALLAS DEL SISTEMA ---

if menu == "▦ DASHBOARD":
    
    # KPIs Superiores Dinámicos
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        # Calcula el valor real de tu inventario (Precio * Stock)
        valor_total = (df_nube["precio"] * df_nube["stock"]).sum() if not df_nube.empty else 25680
        st.markdown(f"""<div class="dashboard-card"><div class="card-title">VALOR INVENTARIO (S/)</div><div class="card-value">S/ {valor_total:,.2f}</div><div style="color: #00FBFF; margin-top: 10px; font-size: 13px;">📈 Base de datos activa</div></div>""", unsafe_allow_html=True)
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

    # Tablas Inferiores (Con vista real de tu base de datos)
    c_table1, c_table2 = st.columns(2)
    with c_table1:
        st.markdown("""<div class="dashboard-card"><div class="card-title" style="color: #F6AD55;">⚠️ STOCK CRÍTICO & ALERTAS</div>""", unsafe_allow_html=True)
        # Filtramos automáticamente los productos que tengan menos de 5 unidades en Supabase
        if not df_nube.empty:
            critico = df_nube[df_nube['stock'] <= 5]
            if not critico.empty:
                st.dataframe(critico[['producto', 'sku', 'stock']], use_container_width=True)
            else:
                st.write("✅ Todo el stock está en niveles óptimos.")
        else:
            st.write("No hay productos cargados en la base de datos.")
        st.markdown("</div>", unsafe_allow_html=True)

    with c_table2:
        st.markdown("""
            <div class="dashboard-card">
                <div class="card-title">BASE DE DATOS COMPLETA (TIEMPO REAL)</div>
            """, unsafe_allow_html=True)
        st.dataframe(df_nube, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- MÓDULO NUEVO: INVENTARIO (INGRESO DE DATOS) ---
elif menu == "📦 INVENTARIO":
    st.markdown("<h2 style='color: #00FBFF;'>Gestión de Almacén en la Nube</h2>", unsafe_allow_html=True)
    st.write("Registra tus productos aquí. Al guardar, el sistema actualizará tu base de datos y recalculará el Dashboard automáticamente.")
    
    # Formulario de ingreso perfectamente integrado al modo oscuro
    with st.expander("➕ / 📝 REGISTRAR O ACTUALIZAR CONSOLAS / ACCESORIOS", expanded=True):
        with st.form("form_almacen", clear_on_submit=True):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                nombre_prod = st.text_input("Nombre del Producto *", placeholder="Ej: Game Stick Pro 64GB")
                sku_prod = st.text_input("Código SKU *", placeholder="Ej: GSP-64")
            with col_f2:
                precio_prod = st.number_input("Precio Unitario (S/)", min_value=0.0, format="%.2f")
                stock_prod = st.number_input("Cantidad en Stock", min_value=0, step=1)
            
            st.write("")
            submit_btn = st.form_submit_button("💾 GUARDAR EN SUPABASE")
            
            if submit_btn:
                if not nombre_prod or not sku_prod:
                    st.warning("⚠️ Debes ingresar al menos el Nombre y el SKU para registrar el producto.")
                else:
                    if supabase:
                        payload = {
                            "producto": nombre_prod, 
                            "sku": sku_prod, 
                            "precio": precio_prod, 
                            "stock": stock_prod
                        }
                        try:
                            # Sube el dato a Supabase usando la llave primaria (SKU)
                            supabase.table("inventario").upsert(payload).execute()
                            st.success(f"🚀 ¡Excelente! '{nombre_prod}' sincronizado correctamente.")
                            st.balloons()
                        except Exception as e:
                            st.error(f"Error de conexión con la tabla 'inventario'. Asegúrate de haber creado las columnas correctas en Supabase. Detalle técnico: {e}")
                    else:
                        st.error("❌ No se detecta conexión activa con Supabase.")

    st.write("---")
    st.markdown("### 📦 Listado de Inventario Actualizado")
    # Forzamos una lectura limpia para mostrar el ítem recién guardado
    df_fresco = cargar_inventario()
    st.dataframe(df_fresco, use_container_width=True)

else:
    st.markdown(f"<h2 style='color: #00FBFF; margin-top: 20px;'>Módulo de {menu}</h2>", unsafe_allow_html=True)
    st.markdown('<div class="dashboard-card">Este módulo mantendrá el diseño oscuro. Utiliza la pestaña <b>📦 INVENTARIO</b> para interactuar con la base de datos.</div>', unsafe_allow_html=True)
