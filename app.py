import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from supabase import create_client

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="SYNTHESIA ERP", layout="wide", page_icon="🕹️")

# --- 2. CONEXIÓN A SUPABASE ---
URL = "https://yalomimyjgaofjsxxtff.supabase.co"
KEY = "sb_publishable_am9lY29ubm9yQGdtYWlsLmNvbToxNzMxOTkyNTQ3Nzg5"

@st.cache_resource
def iniciar_conexion():
    try:
        return create_client(URL, KEY)
    except:
        return None

supabase = iniciar_conexion()

# Función para consultar la base de datos en tiempo real
def cargar_inventario():
    if supabase:
        try:
            res = supabase.table('inventario').select("*").execute()
            if res.data:
                return pd.DataFrame(res.data)
        except:
            pass
    # Estructura vacía de respaldo si no hay datos aún
    return pd.DataFrame(columns=["producto", "sku", "precio", "stock"])

# Cargamos los datos globales
df_inventario = cargar_inventario()
stock_total = df_inventario['stock'].sum() if not df_inventario.empty else 0

# --- 3. CSS AVANZADO (ESTILO NEÓN PREMIUM) ---
st.markdown("""
    <style>
    .stApp { background-color: #12161F !important; }
    .block-container { padding-top: 2rem !important; padding-bottom: 0rem !important; max-width: 100% !important; }
    
    [data-testid="stSidebar"] {
        background-color: #1A202C !important;
        border-right: 1px solid #2D3748 !important;
    }
    
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

# --- 5. VISTAS DEL SISTEMA ---

if menu == "▦ DASHBOARD":
    # KPIs Superiores
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        ventas_totales = (df_inventario["precio"] * df_inventario["stock"]).sum() if not df_inventario.empty else 0
        st.markdown(f"""<div class="dashboard-card"><div class="card-title">VALOR INVENTARIO</div><div class="card-value">S/ {ventas_totales:,.2f}</div><div style="color: #00FBFF; margin-top: 10px; font-size: 13px;">Sincronizado en nube</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="dashboard-card"><div class="card-title">STOCK ACTUAL</div><div class="card-value">{stock_total} <span style="font-size: 14px; color: #A0AEC0;">unidades</span></div><div style="width: 100%; background-color: #2D3748; height: 6px; border-radius: 3px; margin-top: 15px;"><div style="width: 75%; background-color: #00FBFF; height: 6px; border-radius: 3px;"></div></div></div>""", unsafe_allow_html=True)
    with col3:
        productos_activos = len(df_inventario)
        st.markdown(f"""<div class="dashboard-card"><div class="card-title">VARIEDAD DE PRODUCTOS</div><div class="card-value">{productos_activos}</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class="dashboard-card"><div class="card-title">ESTADO SERVIDOR</div><div class="card-value" style="color:#48BB78;">ONLINE</div></div>""", unsafe_allow_html=True)

    st.write("")

    # Gráficos Centrales de demostración visual
    c_chart1, c_chart2, c_chart3 = st.columns([2, 1, 1])
    with c_chart1:
        st.markdown('<div class="dashboard-card"><div class="card-title">FLUJO DE MOVIMIENTOS</div>', unsafe_allow_html=True)
        meses = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(x=meses, y=[12, 15, 8, 20, 18, 25], name='Salidas', marker_color='#00FBFF'))
        fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#A0AEC0', size=10), margin=dict(l=0, r=0, t=10, b=0), height=220)
        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    with c_chart2:
        st.markdown('<div class="dashboard-card"><div class="card-title">DISTRIBUCIÓN</div>', unsafe_allow_html=True)
        fig2 = go.Figure(data=[go.Pie(labels=['Consolas', 'Accesorios'], values=[70, 30], hole=.6, marker_colors=['#00FBFF', '#D53F8C'])])
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#A0AEC0', size=10), margin=dict(l=0, r=0, t=10, b=0), height=220, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    with c_chart3:
        st.markdown('<div class="dashboard-card"><div class="card-title">ACCESOS</div><p style="color:#A0AEC0; font-size:12px;">Sistema listo para operaciones móviles.</p></div>', unsafe_allow_html=True)

    st.write("")
    
    # Vista rápida de la base de datos real en el Dashboard
    st.markdown("### 📋 Vista Previa de Base de Datos")
    st.dataframe(df_inventario, use_container_width=True)

elif menu == "📦 INVENTARIO":
    st.markdown("<h2 style='color: #00FBFF;'>Gestión de Inventario en Nube</h2>", unsafe_allow_html=True)
    st.write("Agrega nuevos productos o actualiza el stock de los existentes. Los cambios se reflejarán al instante.")
    
    # Formulario funcional
    with st.expander("➕ / 📝 AGREGAR O ACTUALIZAR PRODUCTO", expanded=True):
        with st.form("form_inventario", clear_on_submit=True):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                nombre = st.text_input("Nombre del Producto *", placeholder="Ej: Game Stick Pro 64GB")
                sku = st.text_input("Código SKU *", placeholder="Ej: GSP-64")
            with col_f2:
                precio = st.number_input("Precio de Venta (S/)", min_value=0.0, format="%.2f")
                stock = st.number_input("Stock Inicial / Actual", min_value=0, step=1)
            
            st.write("")
            boton_guardar = st.form_submit_button("💾 GUARDAR EN BASE DE DATOS")
            
            if boton_guardar:
                if not nombre or not sku:
                    st.warning("⚠️ Por favor, completa el Nombre y el SKU del producto.")
                else:
                    if supabase:
                        datos = {"producto": nombre, "sku": sku, "precio": precio, "stock": stock}
                        try:
                            # insert o update basado en la configuración de tu tabla en Supabase
                            supabase.table("inventario").upsert(datos).execute()
                            st.success(f"🚀 ¡Éxito! '{nombre}' se guardó correctamente en la nube.")
                            st.balloons()
                        except Exception as e:
                            st.error(f"Error al guardar en la nube: Verifica que la tabla 'inventario' exista y tenga las columnas correctas. Detalles: {e}")
                    else:
                        st.error("❌ No hay conexión activa a Supabase.")

    st.write("---")
    st.write("### 📦 Inventario Consolidado")
    # Forzamos recarga para ver el dato recién ingresado
    df_actualizado = cargar_inventario()
    st.dataframe(df_actualizado, use_container_width=True)

else:
    st.markdown(f"<h2 style='color: #00FBFF; margin-top: 20px;'>Módulo: {menu}</h2>", unsafe_allow_html=True)
    st.markdown('<div class="dashboard-card"><p>Interfaz en desarrollo. Utiliza la pestaña <b>📦 INVENTARIO</b> para gestionar tu base de datos.</p></div>', unsafe_allow_html=True)
