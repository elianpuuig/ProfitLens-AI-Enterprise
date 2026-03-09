import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
import sqlite3
import os
import base64

# --- 1. FUNCIÓN DE CONVERSIÓN (Cerebro del Fondo) ---
@st.cache_data
def get_base64_logo(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()
    return ""

# --- CONTROL DE RESET INSTANTÁNEO ---
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0


# Recuperamos el motor real
engine = st.session_state.motor

# Obtenemos el fondo en base64
bg_b64 = get_base64_logo("static/profitlens_bg.png")

st.markdown("""
    <style>
    /* --- MODIFICACIÓN PARA EL BOTÓN DE SIDEBAR --- */
    [data-testid="stHeader"] {
        background: transparent !important; /* Hacemos el fondo invisible */
        color: #00ff08 !important;         /* Pintamos los iconos de verde */
    }

    /* Forzamos que el icono de "hamburguesa" sea visible y brillante */
    [data-testid="stHeader"] svg {
        fill: #00ff08 !important;
        filter: drop-shadow(0 0 5px rgba(0, 255, 8, 0.5));
    }
    
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    /* Ajuste para que el contenido empiece bien arriba */
    .block-container {
        padding-top: 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. CEREBRO VISUAL (ESTILOS ATMOSFÉRICOS + ANIMACIONES + SIDEBAR) ---
st.markdown(f"""
    <style>
    /* 1. FONDO CON BASE64 (Aquí está el cambio clave) */
    .stApp {{
        background: 
            radial-gradient(circle, rgba(10, 10, 10, 0.4) 0%, rgba(5, 5, 5, 0.95) 100%),
            url("data:image/png;base64,{bg_b64}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        background-repeat: no-repeat;
    }}

    /* 2. ANIMACIÓN DE ENTRADA (FADE-IN UP) - También con dobles llaves */
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(30px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    [data-testid="stVerticalBlock"] > div {{
        animation: fadeInUp 0.8s ease-out forwards;
    }}

    /* 3. ESTILOS DEL SIDEBAR */
    [data-testid="stSidebar"] {{
        background-color: #050505 !important;
        border-right: 1px solid rgba(0, 255, 8, 0.15);
    }}

    /* 4. INPUTS TECNOLÓGICOS */
    .stSelectbox div[data-baseweb="select"], .stTextInput input, div[role="radiogroup"] {{
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(0, 255, 8, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
    }}

    [data-testid="stRadio"] div[role="radiogroup"] {{
        background-color: transparent !important;
        border: none !important;
    }}

    .stButton>button {{
        background: rgba(255, 255, 255, 0.03) !important;
        color: #ffffff !important;
        border: 1px solid rgba(0, 255, 8, 0.4) !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        transition: all 0.3s ease !important;
    }}

    .stButton>button:hover {{
        background: #00ff08 !important;
        color: #000000 !important;
        box-shadow: 0 0 20px rgba(0, 255, 8, 0.4) !important;
    }}

    .ai-response-container {{
        background-color: rgba(0, 255, 8, 0.03);
        border: 1px solid rgba(0, 255, 8, 0.2);
        border-left: 5px solid #00ff08;
        border-radius: 15px;
        padding: 25px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 1. SIDEBAR ---
with st.sidebar:
    # 1. ESTILOS CSS PARA TRANSFORMAR EL SIDEBAR (Diseño Elite)
    st.markdown(f"""
        <style>
        /* Estilo general del contenedor del Sidebar */
        [data-testid="stSidebar"] {{
            background-color: #050505 !important;
            border-right: 1px solid rgba(0, 255, 8, 0.15);
        }}

        /* Efecto de resplandor para los Inputs */
        .stSelectbox div[data-baseweb="select"], .stTextInput input, div[role="radiogroup"] {{
            background-color: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(0, 255, 8, 0.2) !important;
            border-radius: 12px !important;
            color: white !important;
            transition: all 0.3s ease;
        }}
        
        /* ELIMINAMOS EL BORDE DEL RADIO (Origen de Datos) */
        [data-testid="stRadio"] div[role="radiogroup"] {{
            background-color: transparent !important;
            border: none !important;
            gap: 10px;
        }}

        .stSelectbox div[data-baseweb="select"]:hover, .stTextInput input:focus {{
            border-color: #00ff08 !important;
            box-shadow: 0 0 10px rgba(0, 255, 8, 0.2) !important;
        }}

        /* Estilo Premium para el botón de Logout */
        .stButton>button {{
            background: rgba(255, 255, 255, 0.03) !important;
            color: #ffffff !important;
            border: 1px solid rgba(0, 255, 8, 0.4) !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
        }}
        .stButton>button:hover {{
            background: #00ff08 !important;
            color: #000000 !important;
            box-shadow: 0 0 20px rgba(0, 255, 8, 0.4) !important;
            border-color: #00ff08 !important;
        }}
        </style>
    """, unsafe_allow_html=True)

    # 2. AVATAR Y PERFIL (Borde Neón)
    user_email = st.session_state.user_info['email'] if st.session_state.user_info else 'User'
    user_name = user_email.split('@')[0].capitalize()
    plan_status = "Plan Gold 💎" if st.session_state.is_subscribed else "Plan Free ⚡"

    st.markdown(f"""
        <div style="
            display: flex; align-items: center; gap: 15px; padding: 20px; 
            background: linear-gradient(135deg, rgba(0, 255, 8, 0.05) 0%, rgba(10, 10, 10, 0.8) 100%); 
            border-radius: 20px; border: 1px solid rgba(0, 255, 8, 0.3); 
            margin-bottom: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        ">
            <img src="https://ui-avatars.com/api/?name={user_email}&background=00ff08&color=000&bold=true" 
                 style="width: 50px; height: 50px; border-radius: 12px; border: 2px solid #00ff08; box-shadow: 0 0 10px rgba(0,255,8,0.4);">
            <div>
                <p style="margin:0; font-weight:800; color:white; font-size: 1.1rem; letter-spacing: -0.5px;">{user_name}</p>
                <p style="margin:0; font-size: 11px; color:#00ff08; font-weight: 600;">{plan_status}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 3. CONFIGURACIÓN (Iconos y Controles)
    st.markdown("<p style='font-size: 0.8rem; font-weight: 700; color: #666; text-transform: uppercase; margin-bottom: 10px;'>Configuración</p>", unsafe_allow_html=True)
    
    st.session_state.idioma = st.selectbox("🌐 Idioma del Sistema", ["Español", "English"], key="sb_idioma")
    st.session_state.ubicacion = st.text_input("📍 Zona de Operación", value=st.session_state.get('ubicacion', ""), key="ti_ubicacion")
    
    st.divider()

    # 4. ORIGEN DE DATOS (Radio Estilizado)
    # 4. ORIGEN DE DATOS (Con lógica de limpieza para que el cambio funcione)
    st.markdown("<p style='font-size: 0.8rem; font-weight: 700; color: #666; text-transform: uppercase; margin-bottom: 10px;'>Data Engine</p>", unsafe_allow_html=True)
    
    # Definimos las opciones con emojis para la visual
    opciones = ["Excel/CSV 📊", "SQL Database 🗄️"]
    
    # Mostramos el radio
    seleccion = st.radio("🔌 Ingesta de Datos", opciones, key="radio_metodo")

    # --- CORRECCIÓN CRÍTICA ---
    # Limpiamos los emojis para que la variable 'metodo' sea lo que tu app espera (Excel/CSV o SQL Database)
    if "Excel/CSV" in seleccion:
        st.session_state.metodo = "Excel/CSV"
    else:
        st.session_state.metodo = "SQL Database"
    
    # Asignamos a la variable local para que el resto del dashboard cambie
    metodo = st.session_state.metodo

    # 5. CIERRE DE SESIÓN (Pie del Sidebar)
    st.markdown('<div style="height: 15vh;"></div>', unsafe_allow_html=True)
    
    if st.button("🚪 Cerrar Sesión", key="logout_social"):
        st.session_state.clear() 
        st.rerun()


# --- 2. LÓGICA DE DATOS ---
st.title("💎 ProfitLens AI")

try:
    if metodo == "Excel/CSV":
        archivo = st.file_uploader("Subir base de ventas", type=['csv', 'xlsx'], 
                               key=f"file_up_{st.session_state.uploader_key}")
        if archivo:
            if st.session_state.df is None:
                df_raw = engine.load_file(archivo)
                df_l, log = engine.run_audit(df_raw, df_raw.columns[0])
                st.session_state.df = df_l
                st.session_state.log_limpieza = log
    else:
        # --- BLOQUEO GOLD PARA SQL ---
        if st.session_state.is_subscribed:
            c1, c2 = st.columns([2, 1])
            url_sql = c1.text_input("URL SQL", placeholder="sqlite:///datos.db", key="ti_sql_url")
            query_sql = c2.text_input("Consulta", value="SELECT * FROM ventas", key="ti_sql_query")
            if st.button("🔌 Conectar y Cargar", key="btn_sql_conn", use_container_width=True):
                if url_sql: # Validación de seguridad
                    df_raw = engine.load_sql(url_sql, query_sql)
                    if df_raw is not None and not df_raw.empty:
                        df_l, log = engine.run_audit(df_raw, df_raw.columns[0])
                        st.session_state.df = df_l
                        st.session_state.log_limpieza = log
                        st.success("✅ Datos recuperados")
                    else:
                        st.error("❌ No se obtuvieron datos de la base.")
            else:
                st.warning("Escribe una URL de base de datos válida.")
        else:
            st.warning("🔒 La conexión a bases de datos SQL es una función exclusiva **GOLD**.")
            st.info("Utiliza archivos Excel/CSV para el análisis gratuito o activa tu suscripción.")
except Exception as e:
    st.error(f"❌ Error: {e}")

# --- 3. RENDERIZADO DEL PANEL ---
if st.session_state.df is not None:
    df = st.session_state.df
    cols = list(df.columns)
    # --- EN EL BOTÓN DE RESET ---
    if st.button("🔄 Cargar otros datos", key="reset_data", use_container_width=True):
        # 1. Limpiamos los datos
        st.session_state.df = None
        # 2. CAMBIAMOS LA KEY (Esto resetea el uploader al toque)
        st.session_state.uploader_key += 1
        # 3. Limpiamos memorias de IA
        if "res_pareto" in st.session_state: del st.session_state.res_pareto
        if "res_forecast" in st.session_state: del st.session_state.res_forecast
        st.rerun()

    st.subheader("⚙️ Configuración de Análisis")
    cc1, cc2, cc3 = st.columns(3)
    with cc1: sel_fecha = st.selectbox("📅 Columna de Tiempo", cols, key="sel_col_fecha")
    with cc2: sel_valor = st.selectbox("💰 Columna de Valor", [c for c in cols if pd.api.types.is_numeric_dtype(df[c])], key="sel_col_valor")
    with cc3: sel_cat = st.selectbox("📦 Categoría / Producto", cols, key="sel_col_cat")

    # Reemplaza tu bloque de validación por este:
    if len({sel_fecha, sel_valor, sel_cat}) < 3:
        st.warning("⚠️ Las columnas de **Tiempo**, **Valor** y **Categoría** deben ser diferentes entre sí para procesar los datos.")
    
    else:
        try:
            st.session_state.growth_delta = engine.calculate_temporal_growth(df, sel_fecha, sel_valor)
            st.metric("Salud del Negocio", "SUBA" if st.session_state.growth_delta > 0 else "BAJA", f"{st.session_state.growth_delta:.2f}%")
        except: pass

        tab1, tab2, tab3 = st.tabs(["📈 Evolución", "🎯 Pareto", "✨ Forecast"])

        with tab1:
            # Usamos doble corchete [[sel_valor]] para forzar un DataFrame 
            # y renombramos la columna de agregación para evitar colisiones
            df_ev = df.groupby(sel_fecha)[[sel_valor]].sum().rename(columns={sel_valor: 'Total'}).reset_index()
            st.plotly_chart(px.line(df_ev, x=sel_fecha, y='Total', template="plotly_dark", color_discrete_sequence=['#00ff08']), use_container_width=True)
            
        with tab2:
            st.markdown("### Análisis Pareto (Regla del 80/20)")
            df_p = engine.get_pareto_analysis(df, sel_cat, sel_valor)
            
            if df_p is not None and not df_p.empty:
                ganador = df_p.iloc[0][sel_cat]
                st.success(f"🏆 **Producto Ganador:** {ganador}")
                
                fig_p = go.Figure()
                fig_p.add_trace(go.Bar(x=df_p[sel_cat], y=df_p[sel_valor], name="Ventas"))
                fig_p.add_trace(go.Scatter(x=df_p[sel_cat], y=df_p['porcentaje_acumulado'], name="% Acumulado", yaxis="y2", line=dict(color="#00ff08")))
                fig_p.update_layout(template="plotly_dark", yaxis2=dict(overlaying="y", side="right", range=[0, 110]))
                st.plotly_chart(fig_p, use_container_width=True)
                
                # BOTÓN GOLD DENTRO DE PARETO
                # --- MEJORA: Persistencia de Consultoría Pareto ---
                if st.button("🧠 Consultoría Pareto IA", key="btn_ai_pareto", use_container_width=True):
                    if st.session_state.is_subscribed:
                        with st.spinner("Analizando patrones VIP..."):
                            vips = df_p[df_p['porcentaje_acumulado'] <= 85][sel_cat].tolist()
                            prompt = engine.get_ai_insight_prompt(df_p[sel_valor].sum(), 0, vips, "Retail", st.session_state.ubicacion, st.session_state.idioma)
                            # Guardamos en session_state
                            st.session_state.res_pareto = engine.get_ai_analysis(prompt)
                    else:
                        st.error("🔒 Función exclusiva para miembros **GOLD**.")

                # Mostramos el resultado si existe en memoria
                if "res_pareto" in st.session_state:
                    st.markdown(f'<div class="ai-response-container">{st.session_state.res_pareto}</div>', unsafe_allow_html=True)
                    st.download_button("📥 Descargar Reporte Pareto", st.session_state.res_pareto, "Pareto_IA.md", key="dl_pareto")
            else:
                st.info("Configura las columnas correctamente para ver el análisis de Pareto.")

        with tab3:
            st.markdown("### Proyección Forecast IA")
            try:
                # 1. Corregimos el nombre de la función (predict)
                # 2. Forzamos la conversión a fecha antes de enviar al motor
                df_temp = df.copy()
                df_temp[sel_fecha] = pd.to_datetime(df_temp[sel_fecha])
                
                pred = engine.predict_next_month(df_temp, sel_fecha, sel_valor)
                
                
                df_h = df.set_index(pd.to_datetime(df[sel_fecha])).resample('ME')[sel_valor].sum()
                fig_f = go.Figure()
                fig_f.add_trace(go.Scatter(x=df_h.index, y=df_h.values, name="Historial", line=dict(color="#ff7b00")))
                fig_f.add_trace(go.Scatter(x=[df_h.index[-1] + pd.DateOffset(months=1)], y=[pred], name="Predicción", marker=dict(size=12, color="#00ff08", symbol="star")))
                fig_f.update_layout(template="plotly_dark")
                st.plotly_chart(fig_f, use_container_width=True)
                
                st.metric("Resultado Proyectado Próximo Mes", f"${pred:,.2f}")

                # BOTÓN GOLD DENTRO DE FORECAST
                # --- MEJORA: Persistencia de Consultoría Forecast ---
                if st.button("🧠 Consultoría Forecast IA", key="btn_ai_forecast", use_container_width=True):
                    if st.session_state.is_subscribed:
                        with st.spinner("Generando plan de acción..."):
                            prompt = engine.get_ai_insight_prompt(df_h.iloc[-1], pred, [], "Retail", st.session_state.ubicacion, st.session_state.idioma)
                            # Guardamos en session_state
                            st.session_state.res_forecast = engine.get_ai_analysis(prompt)
                    else:
                        st.error("🔒 Plan de Acción IA bloqueado.")

                # Mostramos el resultado si existe en memoria
                if "res_forecast" in st.session_state:
                    st.markdown(f'<div class="ai-response-container">{st.session_state.res_forecast}</div>', unsafe_allow_html=True)
                    st.download_button("📥 Descargar Plan de Acción", st.session_state.res_forecast, "Forecast_IA.md", key="dl_forecast")
            except:
                st.warning("Datos insuficientes para el modelo predictivo.")

    # EXPORTACIÓN AL FINAL
    # --- EXPORT HUB PROFESIONAL (DISEÑO DESTACADO) ---
    st.divider()

    st.markdown("### 🚀 Exportación de Datos de Élite")
    st.write("Selecciona el formato que mejor se adapte a tu necesidad para descargar tu base de datos auditada:")

    # Ponemos los botones justo debajo o dentro de columnas
    if st.session_state.is_subscribed:
        ex1, ex2 = st.columns(2)
        
        # --- LÓGICA EXCEL CON FILTROS ---
        buf = io.BytesIO()
        # Usamos xlsxwriter para darle el toque Pro
        with pd.ExcelWriter(buf, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='ProfitLens_Audit')
            workbook  = writer.book
            worksheet = writer.sheets['ProfitLens_Audit']
            
            # Aplicamos autofiltros a todas las columnas
            (max_row, max_col) = df.shape
            worksheet.autofilter(0, 0, max_row, max_col - 1)
            
            # Opcional: Ajustamos el ancho de columnas (Toque de calidad extra)
            for i, col in enumerate(df.columns):
                worksheet.set_column(i, i, max(len(col), 15))

        with ex1:
            st.markdown("### 📊 Para Negocios")
            st.info("Archivo Excel listo para Excel/Sheets con **filtros automáticos** aplicados.")
            st.download_button(
                label="📥 DESCARGAR EXCEL AUDITADO",
                data=buf.getvalue(),
                file_name="ProfitLens_Maestro.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

        with ex2:
            st.markdown("### 🔌 Para Sistemas")
            st.info("Script SQL para replicar esta base de datos en cualquier sistema de gestión.")
            db_buf = io.BytesIO()
            with sqlite3.connect(':memory:') as conn:
                df.to_sql('profitlens_audit', conn)
                for line in conn.iterdump(): 
                    db_buf.write(f'{line}\n'.encode())
            
            st.download_button(
                label="💾 DESCARGAR SQL DUMP",
                data=db_buf.getvalue(),
                file_name="ProfitLens_Database.sql",
                mime="application/sql",
                use_container_width=True
            )
    else:
        # Versión bloqueada para usuarios Free
        c1, c2 = st.columns(2)
        c1.button("📊 Descargar Excel (Solo GOLD 🔒)", disabled=True, use_container_width=True)
        c2.button("🔌 Descargar SQL (Solo GOLD 🔒)", disabled=True, use_container_width=True)
        st.warning("⚠️ La exportación de datos auditados es una función exclusiva de **ProfitLens Gold**.")