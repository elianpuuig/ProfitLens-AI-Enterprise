import streamlit as st
from services.auth_service import FirebaseAuth
from services.engine import ProfitLensEngine
import stripe


# CONFIGURACIÓN DE PÁGINA (DEBE SER LO PRIMERO)
st.set_page_config(page_title="ProfitLens AI Gold", page_icon="💎", layout="wide")

# --- INICIALIZACIÓN CRÍTICA DE ESTADO ---
def init_all_states():
    defaults = {
        'user_info': None,
        'is_subscribed': False,
        'df': None,
        'log_limpieza': [],
        'growth_delta': 0.0,
        'idioma': "Español",
        'ubicacion': "",
        'perfil': "Retail",
        'last_report_pareto': None,
        'last_report_forecast': None
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

    if 'motor' not in st.session_state:
        api_key = st.secrets.get("GEMINI_API_KEY")
        st.session_state.motor = ProfitLensEngine(api_key=api_key)

init_all_states()

# 3. INSTANCIAR SERVICIOS Y CONFIGURAR STRIPE
auth = FirebaseAuth()
stripe.api_key = st.secrets["stripe"]["secret_key"]
# 4. PROCESAMIENTO DE PAGO (STRIPE -> FIREBASE)
# Priorizamos esto para capturar el pago apenas el usuario vuelve de la pasarela
params = st.query_params
if "session_id" in params:
    try:
        session = stripe.checkout.Session.retrieve(params["session_id"])
        if session.payment_status == "paid":
            # Extraemos el email directamente de Stripe (Blindaje total)
            email_cliente = session.customer_details.email
            sub_id = session.get('subscription')

            # GUARDADO EN FIREBASE
            if auth.activar_suscripcion_gold(email_cliente, sub_id):
                # Si el usuario ya está logueado, impactamos el cambio en vivo
                if st.session_state.user_info and st.session_state.user_info['email'] == email_cliente:
                    st.session_state.is_subscribed = True
                
                st.success(f"¡Suscripción Gold activada para {email_cliente}!")
                st.balloons()
            
            # Limpiamos la URL para evitar re-validaciones innecesarias
            st.query_params.clear()
    except Exception as e:
        st.error(f"Error en la validación de Stripe: {e}")

# 5. VERIFICACIÓN DE PERSISTENCIA (LOGIN -> FIREBASE)
# Si el usuario ya está logueado, verificamos su estatus real en la DB
if st.session_state.user_info and not st.session_state.is_subscribed:
    email_usuario = st.session_state.user_info.get('email')
    if auth.consultar_suscripcion(email_usuario):
        st.session_state.is_subscribed = True

# 6. DEFINICIÓN DE NAVEGACIÓN
landing_page = st.Page("views/landing.py", title="Inicio", icon="🏠")
dashboard_page = st.Page("views/dashboard.py", title="Panel BI", icon="📊")

if st.session_state.user_info is None:
    pg = st.navigation([landing_page])
else:
    pg = st.navigation([dashboard_page])

# 7. EJECUCIÓN FINAL
pg.run()