from google import genai
from google.genai import types

#Usá la clave que generaste en el proyecto ProfitLens-Final-2026
# Usamos la clave del proyecto ProfitLens-Final-2026
# ASEGURATE DE QUE SEA LA QUE EMPIEZA CON AIza...
client = genai.Client(
    api_key="AIzaSyDRLaTx946GYORtRB5HNjgX65mvAgluKKA",
    http_options={'api_version': 'v1'} # ESTA LÍNEA OBLIGA A SALIR DE V1BETA
)
try:
    print("🚀 Iniciando prueba con Gemini 2.5 Flash (El más nuevo de 2026)...")
    # Usamos el modelo que encabeza tu lista de disponibles
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents="Hola, responde: 'ProfitLens AI 2.5 Conectado y listo'"
    )
    print(f"\n✅ RESULTADO: {response.text}")
    
except Exception as e:
    print(f"\n❌ Error técnico: {e}")