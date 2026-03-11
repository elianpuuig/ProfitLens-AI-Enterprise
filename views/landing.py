import streamlit as st
from services.auth_service import FirebaseAuth
import base64
import os

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


@st.cache_data
def get_base64_logo(path):
    """
    Convierte la imagen a base64 para inyectarla directamente en el HTML/CSS.
    Esto garantiza que el logo cargue instantáneamente y sea responsivo.
    """
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()
    return ""

auth = FirebaseAuth()

def enviar_correo_real(nombre, remitente, mensaje_cuerpo):
    # --- CONFIGURACIÓN DE TU CORREO ---
    email_destino = "profitlensoficial@gmail.com"
    # IMPORTANTE: Aquí va una 'App Password' de Google, no tu clave normal
    password_app = st.secrets["email"]["password"] 

    msg = MIMEMultipart()
    msg['From'] = email_destino
    msg['To'] = email_destino # Te lo mandas a vos mismo
    msg['Subject'] = f"NUEVA CONSULTA: {nombre}"

    cuerpo = f"Nombre: {nombre}\nCorreo: {remitente}\n\nMensaje:\n{mensaje_cuerpo}"
    msg.attach(MIMEText(cuerpo, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_destino, password_app)
        server.sendmail(email_destino, email_destino, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    
    
    
    
    
# --- HEADER ELITE (GLASSMORPHISM & FLOATING DESIGN) ---
logo_b64 = get_base64_logo("static/profitlogo.png")


st.markdown(f"""
    <style>
    /* Ocultar el Header nativo de Streamlit (Deploy, Rerun, etc.) */
    header {{
        visibility: hidden;
        height: 0% !important;
    }}

    /* Ocultar el menú de hamburguesa (Settings, Print, etc.) */
    #MainMenu {{
        visibility: hidden;
    }}

    /* Ocultar el footer de Streamlit (Made with Streamlit) */
    footer {{
        visibility: hidden;
    }}

    /* Ajustar el padding superior para que tu Header flotante no se choque con nada */
    .block-container {{
        padding-top: 2rem !important;
    }}
    
    /* 1. RESET DE ENLACES GLOBALES */
    .nav-bar a {{
        text-decoration: none !important;
        color: inherit;
    }}

    /* 2. CONTENEDOR FLOTANTE */
    .nav-bar {{
        position: fixed;
        top: 25px;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        max-width: 1100px;
        background: rgba(15, 15, 15, 0.75);
        backdrop-filter: blur(25px) saturate(200%);
        -webkit-backdrop-filter: blur(25px) saturate(200%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 10px 35px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 9999;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
    }}

    /* 3. ESTILO DE LINKS DE NAVEGACIÓN */
    .nav-links {{
        display: flex;
        gap: 35px;
        align-items: center;
    }}

    .nav-item {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.85rem;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.6);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        letter-spacing: 0.3px;
        position: relative;
    }}

    .nav-item:hover {{
        color: #ffffff;
        filter: drop-shadow(0 0 5px rgba(255,255,255,0.3));
    }}

    /* 4. BOTÓN ACCESO GOLD (ESTILO BOTÓN DE ACCIÓN) */
    .nav-cta {{
        background: linear-gradient(135deg, #00ff08 0%, #00ab05 100%);
        color: #000 !important;
        padding: 10px 22px;
        border-radius: 14px;
        font-weight: 800;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(0, 255, 8, 0.2);
        transition: all 0.3s ease;
    }}

    .nav-cta:hover {{
        transform: scale(1.03);
        box-shadow: 0 6px 20px rgba(0, 255, 8, 0.4);
        filter: brightness(1.1);
    }}

    .header-spacer {{ height: 130px; }}

    /* --- ADAPTACIÓN PARA CELULARES (SAMSUNG A56) --- */
    @media (max-width: 768px) {{
        .nav-bar {{
            width: 95% !important;
            padding: 8px 15px !important;
            top: 15px !important;
        }}
        .nav-links {{
            gap: 15px !important; /* Menos espacio entre botones */
        }}
        .nav-item {{
            font-size: 0.75rem !important; /* Texto más chico */
        }}
        .nav-cta {{
            padding: 8px 12px !important;
            font-size: 0.7rem !important;
            border-radius: 10px !important;
        }}
        .header-spacer {{ height: 100px; }}
    }}
""", unsafe_allow_html=True)

# --- RENDERIZADO DEL HEADER (LO QUE FALTABA) ---
stripe_url = st.secrets["stripe"]["checkout_url"]

st.markdown(f"""
    <div class="nav-bar">
        <img src="data:image/png;base64,{logo_b64}" style="height: 35px;">
        <div class="nav-links">
            <a href="#caracteristicas" class="nav-item">Características</a>
            <a href="#precios" class="nav-item">Precios</a>
            <a href="#contacto" class="nav-item">Contacto</a>
            <a href="{stripe_url}" target="_blank" class="nav-cta">Acceso Gold 💎</a>
        </div>
    </div>
    <div class="header-spacer"></div>
""", unsafe_allow_html=True)

# --- HERO SECTION ELITE (DISEÑO 2026) ---
# --- HERO SECTION ELITE (CORREGIDA) ---
logo_b64 = get_base64_logo("static/profitlogo.png")

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;700;800&display=swap');
    
    /* Usamos doble llave para que Python no crea que son variables */
    .stApp {{
        background-color: #050505 !important;
    }}

    .hero-wrapper {{
        position: relative;
        width: 100%;
        min-height: 550px;
        background: 
            linear-gradient(90deg, #050505 20%, rgba(5, 5, 5, 0.7) 50%, rgba(5, 5, 5, 0.2) 100%),
            url('https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&w=2000&q=80');
        background-size: cover;
        background-position: right center;
        display: flex;
        align-items: center;
        padding: 60px;
        border-radius: 40px;
        margin-bottom: 60px;
        border: 1px solid rgba(255, 255, 255, 0.03);
    }}

    .hero-content {{
        max-width: 650px;
        z-index: 2;
        text-align: left;
    }}

    .hero-title {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 4.8rem;
        font-weight: 800;
        line-height: 1.1;
        letter-spacing: -2px;
        background: linear-gradient(135deg, #ffffff 30%, #00ff08 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 25px;
        filter: drop-shadow(0 10px 20px rgba(0, 255, 8, 0.2));
    }}

    .hero-description {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.3rem;
        color: #b0b0b0;
        line-height: 1.6;
        font-weight: 400;
        margin-bottom: 40px;
        border-left: 3px solid #00ff08;
        padding-left: 25px;
    }}

    @media (max-width: 1024px) {{
        .hero-wrapper {{
            background: #050505; 
            padding: 40px 20px;
            min-height: auto;
        }}
        .hero-title {{ font-size: 3rem; }}
        .hero-description {{ font-size: 1.1rem; }}
    }}
    
    /* --- SOLUCIÓN PARA MÓVILES --- */
    @media (max-width: 768px) {{
        .hero-wrapper {{
            background-position: center !important; /* Centra la imagen */
            padding: 20px !important;               /* Menos padding para ganar espacio */
            min-height: 450px !important;           /* Ajusta la altura */
            background: 
                linear-gradient(0deg, rgba(5, 5, 5, 0.9) 30%, rgba(5, 5, 5, 0.2) 100%), /* Gradiente vertical para móviles */
                url('https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&w=2000&q=80');
            background-size: cover;
        }}
        
        .hero-content {{
            text-align: center !important; /* Centramos el texto en móviles */
            margin: 0 auto;
        }}
    }}
    </style>
    
    <div class="hero-wrapper">
        <div class="hero-content">
            <h1 class="hero-title">ProfitLens<br>AI Gold</h1>
            <p class="hero-description">
                Elevamos la analítica de tu negocio a una dimensión superior. 
                Audita, predice y escala tu rentabilidad con un consultor de 
                IA que vive dentro de tus datos.
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)


# --- 2. GRID PRINCIPAL (VSL Y LOGIN) ---
# --- 3. SECCIÓN CARACTERÍSTICAS (PUNTO DE ANCLAJE) ---
st.markdown("<div id='caracteristicas'></div>", unsafe_allow_html=True)
col1, col2 = st.columns([1.1, 0.9], gap="large")

with col1:
    st.markdown("### 🎥 Mira ProfitLens en acción")
    # Insertalo justo después del título o en la sección de héroe
    # --- LOGICA DEL VIDEO BLINDADA ---
    video_path = "static/promo_video.mp4"

    if os.path.exists(video_path):
        if 'video_visto' not in st.session_state:
            st.video(video_path, autoplay=True, muted=True)
            st.session_state.video_visto = True
        else:
            st.video(video_path, autoplay=False)
    else:
        st.error(f"⚠️ Error: No se encuentra el video en {video_path}")
    st.markdown("""
        <p style='opacity: 0.7; font-size: 0.9rem; margin-top: 15px;'>
            Descubre cómo nuestra IA analiza miles de filas de datos en segundos para darte 
            hojas de ruta estratégicas que antes requerían semanas de consultoría humana.
        </p>
    """, unsafe_allow_html=True)

with col2:
    tab1, tab2 = st.tabs(["🔐 Ingresar", "✨ Registrarme"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email institucional")
            pw = st.text_input("Contraseña", type="password")
            btn_login = st.form_submit_button("🚀 ENTRAR AL PANEL", use_container_width=True)
            
            if btn_login:
                if email and pw:
                    with st.spinner("Verificando credenciales..."):
                        try:
                            # 1. Intentamos el login
                            user = auth.login(email, pw)
                            
                            if user and 'localId' in user:
                                # 2. Si llegamos acá, el login fue exitoso. 
                                # Guardamos los datos críticos primero.
                                st.session_state.user_info = user
                                
                                # 3. Verificamos suscripción con el email (nombre de función correcto)
                                try:
                                    # Usamos 'email' porque tu auth_service pide el correo, no el ID
                                    st.session_state.is_subscribed = auth.consultar_suscripcion(email)
                                except Exception as e:
                                    st.session_state.is_subscribed = False # Default si falla la DB
                                
                                # 4. Marcamos como logueado y reiniciamos
                                st.session_state.logged_in = True
                                st.rerun()
                            else:
                                st.error("No se pudo obtener la información del usuario.")
                                
                        except Exception as e:
                            # Capturamos el error real para no confundir al usuario
                            error_msg = str(e)
                            if "INVALID_PASSWORD" in error_msg or "EMAIL_NOT_FOUND" in error_msg:
                                st.error("📧 Email o contraseña no válidos.")
                            else:
                                st.error("🖥️ Error de conexión con el servidor. Reintenta en un momento.")
                else:
                    st.warning("Por favor, completa ambos campos.")
    with tab2:
        with st.form("reg_form"):
            new_email = st.text_input("Nuevo Email")
            new_pw = st.text_input("Nueva Clave (min. 6 car.)", type="password")
            if st.form_submit_button("💎 CREAR CUENTA GOLD", width="stretch"):
                try:
                    auth.signup(new_email, new_pw)
                    st.success("Cuenta creada con éxito. ¡Verifica tu email e ingresa!")
                except Exception as e:
                    st.error(f"Error: {e}")
  
  
  
# --- SECCIÓN: PITCH DE VENTA ELITE (CORREGIDO) ---
  
# --- 1. DEFINICIÓN DE ESTILOS (EL "STYLE") ---
pitch_style = """
<style>
    .pitch-container { margin: 80px 0; padding: 0 15px; }
    .pitch-title { 
        font-family: 'Plus Jakarta Sans', sans-serif; 
        font-size: 3.2rem; font-weight: 800; line-height: 1.1; 
        color: white; margin-bottom: 45px; letter-spacing: -1.5px; 
    }
    .pitch-border-box { border-left: 3px solid #00ff08; padding-left: 35px; max-width: 850px; }
    .pitch-text-gray { font-size: 1.2rem; color: #b0b0b0; line-height: 1.8; margin-bottom: 25px; }
    .pitch-text-white { font-size: 1.25rem; color: white; line-height: 1.8; margin-bottom: 25px; }
    /* Ajuste para móviles (Samsung A56) - Texto a la IZQUIERDA */
    @media (max-width: 768px) {
        .pitch-title { 
            font-size: 2.3rem !important; 
            text-align: left !important; /* Forzamos izquierda */
        }
        .pitch-border-box { 
            border-left: 2px solid #00ff08 !important; /* Mantenemos la línea verde fina */
            padding-left: 20px !important; 
            text-align: left !important; /* Texto a la izquierda */
        }
        .pitch-container { 
            margin-top: 50px; 
            margin-bottom: 50px; 
            padding-left: 10px; /* Margen mínimo para que no pegue al borde */
        }
    }
</style>
"""

# --- 2. ESTRUCTURA DE LA SECCIÓN (LOS "DIVS") ---
pitch_html = """
<div class="pitch-container">
    <h2 class="pitch-title">
        Tu negocio no necesita <span style="color: rgba(255,255,255,0.4);">más datos</span>.<br>
        Necesita <span style="color: #00ff08;">más Claridad</span>.
    </h2>
    <div class="pitch-border-box">
        <p class="pitch-text-gray">
            En el mercado actual, estar "ciego" ante tus propios números es el camino más rápido al estancamiento. 
            Mientras tu competencia pierde horas en planillas obsoletas, <b>ProfitLens AI</b> te entrega el mapa del tesoro en tiempo real.
        </p>
        <p class="pitch-text-white">
            <span style="color: #00ff08; font-weight: 800; text-transform: uppercase; font-size: 0.85rem; letter-spacing: 2px;">La Ventaja Competitiva:</span><br>
            Identificamos el 20% de stock que genera el 80% de tus ingresos y proyectamos tu crecimiento con modelos de <b>Forecast de última generación</b>.
        </p>
        <p class="pitch-text-gray">
            Llevá tu visión desde <b>Puerto Madryn</b> al mundo. Dejá de adivinar el futuro. <b>Construilo con el Nivel Gold.</b>
        </p>
    </div>
</div>
"""

# --- 3. RENDERIZADO SEGURO ---
st.markdown(pitch_style, unsafe_allow_html=True)
st.markdown(pitch_html, unsafe_allow_html=True)

# --- SECCIÓN DE PRECIOS EVOLUCIONADA (CORREGIDA Y RESPONSIVA) ---
st.write("---")
st.markdown("<h2 id='precios' style='text-align:center; margin-bottom:60px; font-weight:800; letter-spacing:1px;'>ELIGE TU NIVEL DE INTELIGENCIA</h2>", unsafe_allow_html=True)

st.markdown("""
    <style>
    html {
    scroll-behavior: smooth; 
    }
    .price-card {
        background: rgba(255,255,255,0.03);
        padding: 40px 30px;
        border-radius: 28px;
        border: 1px solid #333;
        transition: all 0.4s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
        /* ELIMINAMOS height fijo para que se adapte al contenido */
        height: auto; 
        min-height: 550px;
        display: flex;
        flex-direction: column;
        margin-bottom: 20px; /* Espacio para cuando se apilen en móvil */
    }
    
    .price-card:hover {
        transform: translateY(-5px);
        background: rgba(255,255,255,0.05);
    }
    
    .gold-card {
        border: 2px solid #00ff08 !important;
        box-shadow: 0 0 20px rgba(0, 255, 8, 0.05);
    }
    
    .gold-card:hover {
        box-shadow: 0 0 40px rgba(0, 255, 8, 0.2);
    }

    .feature-list { 
        list-style: none; 
        padding: 0; 
        margin-top: 20px; 
        margin-bottom: 30px;
        flex-grow: 1; /* Esto empuja el botón/footer de la card hacia abajo */
    }

    .feature-list li { 
        margin-bottom: 12px; 
        font-size: 0.95rem; 
        opacity: 0.8; 
        display: flex; 
        align-items: flex-start; 
        gap: 10px; 
    }

    /* Ajuste para pantallas pequeñas (Móvil) */
    @media (max-width: 768px) {
        .price-card {
            min-height: auto;
            padding: 30px 20px;
        }
        .gradient-text {
            font-size: 2.5rem !important;
        }
    }
    </style>
""", unsafe_allow_html=True)


# CSS para Tarjetas Interactivas y Efectos Neón
# --- CSS DINÁMICO ---
st.markdown("""
    <style>
    .price-card {
        background: rgba(255,255,255,0.03);
        padding: 40px 25px;
        border-radius: 24px;
        border: 1px solid #333;
        transition: 0.3s all ease;
        /* AJUSTE CLAVE: Alto automático para evitar cortes */
        height: auto; 
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-bottom: 30px;
    }
    
    /* Media Query para móviles: ajusta el tamaño de la fuente */
    @media (max-width: 768px) {
        .price-card {
            padding: 25px 15px;
        }
        h1 { font-size: 2rem !important; }
    }
    </style>
""", unsafe_allow_html=True)

# Inyectamos el ID para el scroll del Header
st.markdown("<div id='precios'></div>", unsafe_allow_html=True)

col_free, col_gold = st.columns(2, gap="large")

with col_free:
    st.markdown(f"""
        <div class="price-card">
            <h3 style="color: #888; text-transform: uppercase; letter-spacing: 2px;">Plan Explorador</h3>
            <div class="price-tag">$0 <small style="font-size: 1.2rem; color: #666;">/siempre</small></div>
            <p style="color: #aaa; margin-bottom: 25px;">Para emprendedores que recién comienzan su camino de datos.</p>
            <ul class="feature-list">
                <li><span class="check-v">✓</span> Auditoría de Salud del Dato</li>
                <li><span class="check-v">✓</span> Normalización Unicode de Nombres</li>
                <li><span class="check-v">✓</span> Limpieza de Duplicados</li>
                <li><span class="check-v">✓</span> Gráfico de Evolución Temporal</li>
                <li><span class="check-v">✓</span> Análisis de Pareto Visual</li>
                <li><span class="check-v">✓</span> Conexión de Archivos CSV/Excel</li>
                <li><span class="check-x">✕</span> Consultoría Estratégica IA</li>
                <li><span class="check-x">✕</span> Plan de Acción Forecast IA</li>
                <li><span class="check-x">✕</span> Exportación Profesional Excel</li>
                <li><span class="check-x">✕</span> Volcado de Base de Datos SQL</li>
                <li><span class="check-x">✕</span> Soporte Prioritario</li>
            </ul>
            <div style="text-align: center; color: #555; font-size: 0.8rem;">REGÍSTRATE GRATIS ARRIBA</div>
        </div>
    """, unsafe_allow_html=True)

with col_gold:
    stripe_url = st.secrets["stripe"]["checkout_url"]
    st.markdown(f"""
        <div class="price-card gold-card">
            <a href="{stripe_url}" target="_blank" class="overlay-link"></a>
            <h3 style="color: #00ff08; text-transform: uppercase; letter-spacing: 2px;">Membresía GOLD 💎</h3>
            <div class="price-tag" style="color: #fff;">$14.99 <small style="font-size: 1.2rem; color: #00ff08;">/mes</small></div>
            <p style="color: #eee; margin-bottom: 25px;"><b>Poder total:</b> Transforma ProfitLens en tu consultor de negocios 24/7.</p>
            <ul class="feature-list">
                <li><span class="check-v">✓</span> <b>TODO lo del Plan Explorador</b></li>
                <li><span class="check-v">✓</span> <b>Consultoría IA Pareto Personalizada</b></li>
                <li><span class="check-v">✓</span> <b>Forecast IA (Predicción de Ventas)</b></li>
                <li><span class="check-v">✓</span> <b>Plan de Acción Estratégico Mensual</b></li>
                <li><span class="check-v">✓</span> <b>Descarga de Excel Auditado Pro</b></li>
                <li><span class="check-v">✓</span> <b>Exportación de Base de Datos SQL</b></li>
                <li><span class="check-v">✓</span> Conexión de Bases de Datos SQLite</li>
                <li><span class="check-v">✓</span> Soporte Estratégico vía Email</li>
                <li><span class="check-v">✓</span> Acceso a Futuras Actualizaciones</li>
                <li><span class="check-v">✓</span> Reportes en PDF/Markdown</li>
            </ul>
            <a href="{stripe_url}" target="_blank" style="text-decoration: none;">
            <div style="background: #00ff08; color: black; text-align: center; padding: 15px; border-radius: 12px; font-weight: 800; font-size: 1.1rem; box-shadow: 0 4px 15px rgba(0,255,8,0.3);">
                🚀 CLICK PARA ACTIVAR AHORA
            </div>
            </a>
        </div>
    """, unsafe_allow_html=True)
    
    
    
# --- SECCIÓN DE CONTACTO ---


st.markdown("<div id='contacto' style='margin-top: 100px;'></div>", unsafe_allow_html=True)
st.divider()

col_info, col_form = st.columns([1, 1.2], gap="large")

with col_info:
    st.markdown("""
        <h2 style='font-size: 2.5rem; margin-bottom: 20px;'>Hablemos de tu <span style='color: #00ff08;'>Escalabilidad</span></h2>
        <p style='opacity: 0.8; font-size: 1.1rem; line-height: 1.6;'>
            Ya seas un líder empresarial o un emprendedor global, nuestro equipo de soporte 
            está listo para asistirte en la implementación de decisiones basadas en datos.
        </p>
        <div style='margin-top: 40px;'>
            <p style='color: #00ff08; font-weight: 800; margin-bottom: 5px;'>EMAIL OFICIAL</p>
            <p style='font-size: 1.2rem; font-weight: 700;'>profitlensoficial@gmail.com</p>
        </div>
        <div style='margin-top: 20px;'>
            <p style='color: #00ff08; font-weight: 800; margin-bottom: 5px;'>DISPONIBILIDAD</p>
            <p style='font-size: 1.1rem; opacity: 0.8;'>Soporte IA 24/7 | Respuesta Humana </p>
        </div>
    """, unsafe_allow_html=True)

with col_form:
    st.markdown("""
        <style>
        /* Estilizamos el formulario nativo para que parezca el premium */
        [data-testid="stForm"] {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 24px !important;
            padding: 30px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.form("contacto_final", clear_on_submit=True):
        st.markdown("<h4 style='color:white;'>Envíanos un mensaje directo</h4>", unsafe_allow_html=True)
        
        nombre = st.text_input("Tu Nombre Completo", placeholder="Ej: Elián Puig")
        correo = st.text_input("Correo Electrónico", placeholder="ejemplo@mail.com")
        mensaje = st.text_area("¿Cómo podemos ayudarte?", placeholder="Escribe tu consulta aquí...")
        
        # Botón con estilo
        submit = st.form_submit_button("🚀 ENVIAR CONSULTA ESTRATÉGICA", use_container_width=True)
        
        if submit:
            if nombre and correo and mensaje:
                with st.spinner("Enviando consulta estratégica..."):
                    exito = enviar_correo_real(nombre, correo, mensaje)
                    if exito:
                        st.balloons()
                        st.success(f"✅ ¡Recibido! Revisaremos tu caso en profitlensoficial@gmail.com")
                    else:
                        st.error("❌ Hubo un error técnico. Por favor, escribinos directo a nuestro mail.")


# --- FOOTER PROFESIONAL Y BLINDADO (ANTI-COPY) ---
st.markdown("""
    <style>
    /* Desactivar la selección de texto en el footer para evitar copias rápidas */
    .no-copy {
        user-select: none;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
    }
    
    .footer-container {
        margin-top: 100px;
        padding: 50px 20px;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        text-align: center;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    </style>

    <div class="footer-container no-copy">
        <div style="margin-bottom: 25px;">
            <span style="font-weight: 800; font-size: 1.4rem; color: #fff;">ProfitLens <span style="color: #00ff08;">AI</span></span>
            <p style="color: #666; font-size: 0.85rem; margin-top: 10px;">
               <b>TÉRMINOS Y CONDICIONES:</b> El uso de ProfitLens AI implica la aceptación de que todos los análisis, predicciones 
            y reportes generados por el motor de Inteligencia Artificial son de carácter puramente informativo. 
            Este software no constituye asesoría financiera, contable o legal profesional. 
            El desarrollador no asume responsabilidad alguna por decisiones empresariales, variaciones en la rentabilidad 
            o pérdidas económicas derivadas de la interpretación de los datos. La precisión de los resultados está 
            sujeta a la integridad de la fuente de datos cargada por el usuario. Al acceder, usted renuncia a cualquier 
            derecho de reclamo o acción legal contra la entidad propietaria de ProfitLens AI.
            </p>
            <p style="color: #666; font-size: 0.85rem; margin-top: 10px;">
                © 2026 ProfitLens AI Enterprise - Todos los derechos reservados.
            </p>
        </div>

       
    </div>
""", unsafe_allow_html=True)