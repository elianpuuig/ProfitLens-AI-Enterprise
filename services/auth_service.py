import requests
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os

# --- 1. INICIALIZACIÓN INTELIGENTE ---
if not firebase_admin._apps:
    try:
        # Opción A: Estamos en la nube (Streamlit Cloud)
        if "firebase_service_account" in st.secrets:
            # Convertimos los secretos a un diccionario de Python
            creds_dict = dict(st.secrets["firebase_service_account"])
            
            # Limpieza técnica de la clave privada (asegura los saltos de línea)
            if "\\n" in creds_dict["private_key"]:
                creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
            
            cred = credentials.Certificate(creds_dict)
            firebase_admin.initialize_app(cred)
            
        # Opción B: Estamos en local (Tu computadora)
        else:
            ruta_llave = os.path.join("ClavePrivada", "claveFirebase.json")
            if os.path.exists(ruta_llave):
                cred = credentials.Certificate(ruta_llave)
                firebase_admin.initialize_app(cred)
            else:
                st.error("⚠️ No se encontró la llave de Firebase en local ni en la nube.")
                
    except Exception as e:
        st.error(f"Error crítico al conectar con Firebase: {e}")

db = firestore.client()

class FirebaseAuth:
    def __init__(self):
        self.api_key = st.secrets["firebase"]["api_key"]
        self.base_url = "https://identitytoolkit.googleapis.com/v1/accounts"

    def login(self, email, password):
        """Inicia sesión con captura atómica de errores."""
        url = f"{self.base_url}:signInWithPassword?key={self.api_key}"
        r = requests.post(url, json={"email": email, "password": password, "returnSecureToken": True})
        if r.status_code == 200:
            return r.json()
        raise Exception("Credenciales inválidas")

    def signup(self, email, password):
        url = f"{self.base_url}:signUp?key={self.api_key}"
        r = requests.post(url, json={"email": email, "password": password, "returnSecureToken": True})
        if r.status_code == 200:
            return r.json()
        raise Exception(r.json().get('error', {}).get('message', 'Error al registrar'))
    
    def activar_suscripcion_gold(self, email, subscription_id):
        """Guarda permanentemente el estado Gold en Firestore."""
        try:
            user_ref = db.collection("usuarios").document(email)
            user_ref.set({
                "is_subscribed": True,
                "subscription_id": subscription_id,
                "plan": "Gold",
                "fecha_pago": firestore.SERVER_TIMESTAMP
            }, merge=True)
            return True
        except Exception as e:
            print(f"Error Firestore: {e}")
            return False

    def consultar_suscripcion(self, email):
        """Revisa si el usuario ya es Gold en la base de datos."""
        try:
            doc = db.collection("usuarios").document(email).get()
            return doc.to_dict().get("is_subscribed", False) if doc.exists else False
        except:
            return False