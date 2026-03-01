import streamlit as st
import pandas as pd
import plotly.express as px
from engine import ProfitLensEngine
import numpy as np
import plotly.graph_objects as go
import os
import io #para que el usuario exporte un excel profecional
import sqlite3 ##para que el usuario exporte un sqlite profecional
import base64

# --- CONFIGURACIÓN DE PÁGINA ---
# 1. Definición de la ruta del logo
logo_path = "static/profitlogo.png"

# 2. Configuración de página (DEBE ser el primer comando de Streamlit)
st.set_page_config(
    page_title="ProfitLens AI Gold",
    page_icon=logo_path if os.path.exists(logo_path) else "💎",
    layout="wide"
)

# --- INICIALIZACIÓN DE COMPONENTES ---
if 'motor' not in st.session_state:
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
        if api_key:
            st.session_state.motor = ProfitLensEngine(api_key=api_key)
        else:
            st.error("⚠️ La clave GEMINI_API_KEY está vacía en secrets.toml")
            st.stop()
    except Exception as e:
        st.error(f"⚠️ Error al leer los secretos: {e}")
        st.stop()

if 'df' not in st.session_state:
    st.session_state.df = None

# --- LÓGICA DE CACHÉ PARA LA IA ---
@st.cache_data(show_spinner=False)
def pedir_analisis_ia(prompt):
    """Esta función guarda la respuesta en memoria. Si el prompt no cambia, no gasta API."""
    return st.session_state.motor.get_ai_analysis(prompt)

def inyectar_estilo_css():
    st.markdown("""
        <style>
        div[data-baseweb="select"] > div, .stButton button, .stDownloadButton button { cursor: pointer !important; }
        .stTabs [data-baseweb="tab-list"] { gap: 15px; padding-bottom: 10px; }
        .stTabs [data-baseweb="tab"] {
            height: auto;
            padding: 12px 25px !important;
            background-color: #1e1e1e;
            border-radius: 8px 8px 0px 0px;
            color: #ffffff;
            font-weight: 500;
            transition: all 0.3s ease;
            border: 1px solid #333;
        }
        .stTabs [data-baseweb="tab"]:hover { background-color: #333333; color: #00ff08; border-color: #00ff08; }
        .stTabs [aria-selected="true"] {
            background-color: #262626 !important;
            color: #00ff08 !important;
            border-bottom: 3px solid #00ff08 !important;
        }
        div[data-testid="stMetric"] { padding: 15px; background-color: #1e1e1e; border-radius: 10px; }
        </style>
    """, unsafe_allow_html=True)

         
def handle_reports():
    # Solo mostramos el contenedor si hay algún reporte generado
    report_pareto = st.session_state.get('last_report_pareto')
    report_forecast = st.session_state.get('last_report_forecast')

    if report_pareto or report_forecast:
        st.divider()
        st.subheader("📥 Centro de Reportes Estratégicos")
        
        if report_pareto:
            with st.container(border=True):
                st.markdown("### 🎯 Análisis de Productos Estrella")
                st.markdown(report_pareto)
                st.download_button("Descargar Análisis Pareto", report_pareto, "pareto.md", key="dl_p")
        
        if report_forecast:
            with st.container(border=True):
                st.markdown("### 📈 Plan de Proyección Mensual")
                st.markdown(report_forecast)
                st.download_button("Descargar Plan Forecast", report_forecast, "forecast.md", key="dl_f")
                

def render_interface():
    # --- HEADER CON SEMÁFORO ---
    with st.container():
        c1, c2 ,c3 = st.columns([2,1, 1])
        with c1:
            st.title("💎 ProfitLens AI")
            st.caption("Enterprise Business Intelligence | v2.5")
        with c2:
            # Selector de Idioma
            st.session_state.idioma = st.selectbox("🌐 Language", ["Español", "English"])
        with c3:
            # Lógica del Semáforo de Salud
            if st.session_state.get('growth_delta', 0) > 0:
                st.markdown("🟢 **Salud: Crecimiento**")
            elif st.session_state.get('growth_delta', 0) > -15:
                st.markdown("🟡 **Salud: Estable**")
            else:
                st.markdown("🔴 **Salud: Riesgo Crítico**")

    # --- SECCIÓN SOBRE PROFITLENS ---
    with st.expander("📖 ¿Qué es ProfitLens AI?"):
        st.write("""
        Transformamos datos crudos en decisiones estratégicas mediante **Machine Learning** y **Pareto**. 
        Nuestra misión es que el dueño del negocio deje de adivinar y empiece a liderar con datos.
        """)
    
    # --- CONFIGURACIÓN DE INTELIGENCIA DE MERCADO ---
    with st.container(border=True):
        st.markdown("### 🧠 Inteligencia de Mercado")
        st.caption("Configura estos datos para que el Consultor IA sea más preciso en sus consejos.")
        
        c1, c2 = st.columns(2)
        with c1:
            st.session_state.perfil = st.selectbox(
                "🎯 Perfil de Negocio", 
                ["Retail", "E-commerce", "Servicios Profesionales", "SaaS", "Industria"]
            )
        with c2:
            # Ubicación opcional con texto de ayuda
            st.session_state.ubicacion = st.text_input(
                "📍 Tu Ubicación (Opcional)", 
                placeholder="Ej: Puerto Madryn, Argentina",
                help="Proporcionar tu ciudad y país permite a la IA analizar competidores locales y clima económico regional."
            )
        
        if not st.session_state.ubicacion:
            st.info("💡 **Tip:** Si indicas tu ubicación, la IA podrá darte tácticas de marketing específicas para tu ciudad.")
            
            
            
def export_data_module(df_limpio):
    st.divider()
    st.subheader("📤 Exportación de Alta Disponibilidad")
    if st.session_state.get('is_subscribed'):
        #Verificamos si esta subscripto para descargar sus bd limpias
        c1, c2 = st.columns(2)
        with c1:
            # --- EXCEL PROFESIONAL ---
            # Creamos un buffer en memoria para el Excel real
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df_limpio.to_excel(writer, index=False, sheet_name='Datos_Auditados')
            
            st.download_button(
                label="📊 Descargar Excel Profesional (.xlsx)",
                data=buffer.getvalue(),
                file_name="ProfitLens_Report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        with c2:
            # --- BASE DE DATOS SQLITE (.db) ---
            # Creamos la base de datos en un buffer de bytes
            conn = sqlite3.connect(':memory:')
            df_limpio.to_sql('ventas_auditadas', conn, index=False)
            
            # Leemos los bytes de la base de datos en memoria
            db_bytes = io.BytesIO()
            for line in conn.iterdump():
                db_bytes.write(f'{line}\n'.encode('utf-8'))
            
            st.download_button(
                label="🔌 Descargar Base de Datos SQL (.db)",
                data=db_bytes.getvalue(),
                file_name="ProfitLens_Database.db",
                mime="application/x-sqlite3",
                key="btn_sql_pro"
            )
    else:
        with st.container(border=True):
            st.warning("🔒 **Función Gold:** La exportación de datos auditados en formato Excel y SQL está reservada para suscriptores.")
            st.info("Suscribite en la barra lateral para descargar tus reportes listos para auditoría.")
            st.button("🔓 Desbloquear Exportaciones", key="lock_export", disabled=True)

# 3. Función avanzada para renderizar el logo en la UI sin pérdida de calidad
def render_sidebar_logo(image_path, width="120px"):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data).decode()
        
        # HTML/CSS para control total de nitidez (tipo object-fit)
        html = f"""
            <div style="display: flex; justify-content: center; margin-bottom: 25px;">
                <img src="data:image/png;base64,{encoded}" 
                     style="width: {width}; 
                            height: auto; 
                            object-fit: contain; 
                            image-rendering: -webkit-optimize-contrast; 
                            image-rendering: crisp-edges;">
            </div>
        """
        st.sidebar.markdown(html, unsafe_allow_html=True)

def ejecutar_consultoria_ia(v_actual, v_pred, vips, clave_reporte):
    """Lógica unificada y blindada para llamar a la IA."""
    with st.chat_message("assistant", avatar="💎"):
        with st.spinner("Consultor ProfitLens analizando el mercado..."):
            # .get() evita errores si el usuario no tocó los selectores todavía
            perfil = st.session_state.get('perfil', 'General')
            ubicacion = st.session_state.get('ubicacion', '')
            idioma = st.session_state.get('idioma', 'Español')
            try:
                # Generamos el prompt pasando ahora el 6to argumento: idioma
                prompt = st.session_state.motor.get_ai_insight_prompt(
                    v_actual, v_pred, vips, perfil, ubicacion, idioma
                )
                
                # Llamamos al análisis (que ya tiene los try-except de errores)
                respuesta = st.session_state.motor.get_ai_analysis(prompt)
                
                # Guardamos y mostramos
                st.session_state[clave_reporte] = respuesta
                st.markdown(respuesta)
                
            except Exception as e:
                # Si algo falla de forma inesperada
                st.error("🚀 **ProfitLens AI:** El motor está experimentando una alta carga. Por favor, reintenta en 60 segundos.")          
                
                
def gestion_suscripcion():
   # Extraemos el link de tus secretos seguros
    stripe_url = st.secrets["stripe"]["checkout_url"]
    
    st.sidebar.divider()
    # render_sidebar_logo("static/profitlogo.png", width="100px") # Opcional: un logo pro
    st.sidebar.subheader("💎 Membresía ProfitLens Gold")
    
    # Estado de suscripción inicial
    if "is_subscribed" not in st.session_state:
        st.session_state.is_subscribed = False

    if not st.session_state.is_subscribed:
        st.sidebar.warning("🔒 Funciones Premium Bloqueadas")
        st.sidebar.write("Activá el motor **Gemini 2.5 Flash** para obtener estrategias personalizadas.")
        
        # EL BOTÓN DE PAGO REAL
        st.sidebar.link_button("🚀 Activar Plan Gold ($14.99)", stripe_url, use_container_width=True)
        
        st.sidebar.caption("💡 Una vez realizado el pago, la consultoría IA se desbloqueará automáticamente en esta sesión.")
    else:
        st.sidebar.success("✅ Suscripción Gold Activa")
        st.sidebar.info("Consultor Estratégico IA: Online")
           
def main():
    inyectar_estilo_css() 
    render_interface()
    st.title("💎 ProfitLens AI: Business Intelligence")
    
    # --- 1. INGESTA DE DATOS (HÍBRIDA) ---
    
    logo_path = "static/profitlogo.png"
    if os.path.exists(logo_path):
        # Definimos un ancho fijo (ejemplo: 150 píxeles) para que no sea gigante
        render_sidebar_logo(logo_path, width="120px")
        
    else:
        st.sidebar.warning("🖼️ Logo no encontrado en /static")
        st.sidebar.subheader("💎 ProfitLens AI Gold")
        
    gestion_suscripcion()
    st.sidebar.subheader("🔌 Fuente de Datos")
    metodo = st.sidebar.radio("Seleccionar origen:", ["Excel/CSV", "SQL Database"])
    
    # RESET LÓGICO: Si cambia el método, limpiamos reportes
    if "last_metodo" not in st.session_state:
        st.session_state.last_metodo = metodo
    if st.session_state.last_metodo != metodo:
        st.session_state.df = None
        st.session_state.last_report_pareto = None
        st.session_state.last_report_forecast = None
        st.session_state.last_metodo = metodo
        
    df_raw = None 

    if metodo == "Excel/CSV":
        archivo_temp = st.sidebar.file_uploader("Cargar archivo", type=['csv', 'xlsx'])
        if archivo_temp:
            with st.spinner("Leyendo archivo..."):
                try:
                    df_raw = st.session_state.motor.load_file(archivo_temp)
                except Exception as e:
                    st.sidebar.error(f"Error al leer Excel: {e}")
    else:
        url_sql = st.sidebar.text_input("URL o Ruta .db", placeholder="sqlite:///datos.db")
        query_sql = st.sidebar.text_input("Consulta SQL", value="SELECT * FROM ventas")
        
        if st.sidebar.button("🔌 Conectar a Base de Datos"):
            with st.spinner("Estableciendo conexión SQL..."):
                try:
                    df_raw = st.session_state.motor.load_sql(url_sql, query_sql)
                    st.sidebar.success("✅ Conexión SQL exitosa")
                    st.toast("Base de datos conectada correctamente", icon="🔌")
                except Exception as e:
                    st.sidebar.error(f"Error de conexión: {e}")

    # --- 2. PROCESAMIENTO UNIFICADO ---
    if df_raw is not None:
        with st.spinner("Ejecutando auditoría y salud del dato..."):
            try:
                columnas = list(df_raw.columns)
                col_f_prob = next((c for c in columnas if any(x in c.lower() for x in ['fecha', 'date'])), columnas[0])
                col_v_prob = next((c for c in columnas if any(x in c.lower() for x in ['venta', 'precio', 'total'])), columnas[-1])

                df_limpio, log_auditoria = st.session_state.motor.run_audit(df_raw, col_f_prob)
                
                st.session_state.df = df_limpio
                st.session_state.log_limpieza = log_auditoria
                st.session_state.growth_delta = st.session_state.motor.calculate_temporal_growth(df_limpio, col_f_prob, col_v_prob)
            except Exception as e:
                st.error(f"Error procesando la fuente: {e}")

    # --- 3. DASHBOARD Y ANÁLISIS (ESTO ES LO QUE FALTABA) ---
    if st.session_state.df is not None:
        df = st.session_state.df
        
        # --- SECCIÓN A: SALUD DEL DATO ---
        st.subheader("🩺 Reporte de Salud de Datos")
        with st.expander("📝 Ver Log de Auditoría"):
            for entrada in st.session_state.log_limpieza:
                st.write(entrada)

        with st.container(border=True):
            c1, c2, c3 = st.columns(3)
            c1.metric("📊 Filas Auditadas", f"{len(df):,}")
            c2.metric("🛡️ Calidad", "100%" if not st.session_state.log_limpieza else "Auditado")
            c3.metric("📂 Columnas", len(df.columns))
            st.divider()

        # --- SECCIÓN B: SELECTORES DINÁMICOS ---
        columnas = list(df.columns)

        # FILTRO ESTRICTO: Solo columnas que Pandas reconozca como fecha o tengan 'fecha'/'date' en el nombre
        cols_fecha = [c for c in columnas if pd.api.types.is_datetime64_any_dtype(df[c]) or any(x in c.lower() for x in ['fecha', 'date'])]

        # FILTRO ESTRICTO: Solo columnas que sean números reales para métricas de valor
        cols_valor = [c for c in columnas if pd.api.types.is_numeric_dtype(df[c])]

        if not cols_fecha: cols_fecha = columnas  # Fallback
        if not cols_valor: cols_valor = columnas  # Fallback

        col_f, col_v, col_c = st.columns(3)
        with col_f: 
            sel_fecha = st.selectbox("📅 Eje Temporal (Solo Fechas)", cols_fecha, help="Selecciona la columna cronológica")
        with col_v: 
            sel_valor = st.selectbox("💰 Métrica de Valor", cols_valor, help="Selecciona la columna con importes o cantidades")
        with col_c: 
            sel_cat = st.selectbox("📦 Categoría / Productos", columnas)

        # --- SECCIÓN C: TABS DE ANÁLISIS ---
        tab1, tab2, tab3 = st.tabs(["📈 Crecimiento", "🎯 Pareto", "✨🎈 Forecast IA"])

        with tab1:
            try:
                delta = st.session_state.motor.calculate_temporal_growth(df, sel_fecha, sel_valor)
        
                # Formato condicional: Si es una locura de crecimiento, avisamos.
                label_mom = "Crecimiento Mensual (MoM)"
                if delta > 500:
                    st.info("🚀 Se detectó un crecimiento excepcional este mes.")
                    
                st.metric(label_mom, f"{delta:,.2f}%", delta=f"{delta:,.2f}%")
                df_ev = df.copy()
                df_ev[sel_fecha] = pd.to_datetime(df_ev[sel_fecha])
                fig_ev = px.line(df_ev.groupby(sel_fecha)[sel_valor].sum().reset_index(), x=sel_fecha, y=sel_valor, template="plotly_dark")
                st.plotly_chart(fig_ev, use_container_width=True)
            except: st.warning("Ajustá las columnas para el análisis temporal.")

        with tab2:
            try:
                df_p = st.session_state.motor.get_pareto_analysis(df, sel_cat, sel_valor)
                fig_p = go.Figure()
                fig_p.add_trace(go.Bar(x=df_p[sel_cat], y=df_p[sel_valor], name="Ventas", marker=dict(color='#3b82f6')))
                fig_p.add_trace(go.Scatter(x=df_p[sel_cat], y=df_p['porcentaje_acumulado'], name="% Acum.", yaxis="y2", line=dict(color="#ef4444", width=3)))
                fig_p.update_layout(template="plotly_dark", yaxis2=dict(overlaying="y", side="right", range=[0, 110]))
                st.plotly_chart(fig_p, use_container_width=True)
                
                vips_raw = df_p[df_p['porcentaje_acumulado'] <= 85][sel_cat].tolist()
                vips = [str(item) for item in vips_raw]
                st.success(f"🌟 **Productos Estrella:** {', '.join(vips)}.")
                                
                # Reemplazá el bloque del botón de Pareto por este:
                if st.session_state.get('is_subscribed'):
                    if st.button("🧠 Generar Consultoría Estratégica", key="btn_pareto"):
                        ejecutar_consultoria_ia(0, 0, vips, 'last_report_pareto')
                else:
                    with st.container(border=True):
                        st.markdown("### 🔒 Análisis Estratégico Bloqueado")
                        st.write("Nuestro Consultor IA ha identificado oportunidades críticas en tus productos estrella, pero necesitas el **Plan Gold** para ver el plan de acción.")
                        st.button("🔓 Desbloquear con Plan Gold", key="lock_pareto", disabled=True)
                        
            except: st.info("Selecciona columnas para Pareto.")

        with tab3:
            try:
                pred = st.session_state.motor.redict_next_month(df, sel_fecha, sel_valor)
                df_hist = df.copy()
                df_hist[sel_fecha] = pd.to_datetime(df_hist[sel_fecha])
                df_agrupado = df_hist.set_index(sel_fecha).resample('ME')[sel_valor].sum()
                val_actual = df_agrupado.iloc[-1]
                
                c1, c2 = st.columns(2)
                c1.metric("Ventas Actuales", f"${val_actual:,.2f}")
                c2.metric("Predicción IA", f"${pred:,.2f}", delta=f"{pred-val_actual:,.2f}")
                
                fig_f = go.Figure()
                fig_f.add_trace(go.Scatter(x=df_agrupado.index, y=df_agrupado.values, name="Historial", line=dict(color="#ff7b00")))
                fecha_f = df_agrupado.index[-1] + pd.DateOffset(months=1)
                fig_f.add_trace(go.Scatter(x=[fecha_f], y=[pred], name="Predicción", marker=dict(size=12, color="#00ff08", symbol="star")))
                fig_f.update_layout(template="plotly_dark", title="Proyección de Ventas")
                st.plotly_chart(fig_f, use_container_width=True)

                if st.session_state.get('is_subscribed'):
                    if st.button("🧠 Generar Plan de Acción Forecast", key="btn_forecast"):
                        vips_ia_raw = st.session_state.motor.get_pareto_analysis(df, sel_cat, sel_valor)[sel_cat].head(3).tolist()
                        vips_ia = [str(item) for item in vips_ia_raw] 
                        ejecutar_consultoria_ia(val_actual, pred, vips_ia, 'last_report_forecast')
                else:
                    with st.container(border=True):
                        st.markdown("### 🔒 Plan de Proyección Bloqueado")
                        st.write("La IA ha calculado tu crecimiento para el próximo mes. Suscribite para ver las tácticas de marketing recomendadas para alcanzar ese objetivo.")
                        st.button("🔓 Desbloquear con Plan Gold", key="lock_forecast", disabled=True)
            except Exception as e: st.error(f"Error en Forecast: {e}")

        # --- 4. EXPORTACIÓN Y REPORTES ---
        handle_reports() # Centro de reportes estratégico
        export_data_module(df)

    st.divider()
    st.caption("© 2026 ProfitLens AI Enterprise | Powered by Elián Puig - Data Science & AI")
    
    
if __name__ == "__main__":
    main()
    
    

    
    
