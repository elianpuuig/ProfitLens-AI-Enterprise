import requests
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os

# 1. INICIALIZACIÓN (Fuera de la clase para que ocurra una sola vez)
# RUTA CORRECTA SEGÚN TU INDICACIÓN
ruta_llave = os.path.join("ClavePrivada", "claveFirebase.json")

if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(ruta_llave)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Error crítico al cargar credenciales de Firebase: {e}")

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