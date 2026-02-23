"""👨‍🏫 Lección 1: La Normalización de Strings (El Motor de Identidad)
Como Científico de Datos, el primer problema que enfrentás es que los datos vienen "sucios". Si en tu base de datos tenés "Smartphone X", "smartphone x " y "Smartphóne X", para una computadora son tres cosas distintas, pero para el negocio es la misma. Si no normalizás, tus reportes de ventas van a estar divididos y erróneos.

Lógica de Ingeniería: Usamos Normalización Unicode y expresiones regulares. La idea es llevar todo a su forma más básica (minúsculas, sin espacios extra, sin acentos)."""
import unicodedata
import pandas as pd
from sqlalchemy import create_engine, text
import numpy as np
import streamlit as st
from google import genai


class ProfitLensEngine:
    def __init__(self, api_key):
        """
        Inicialización optimizada para 2026.
        Elimina dependencias de google-generativeai.
        """
        if api_key:
            # 1. Agregamos las http_options para forzar la versión v1 estable
            self.client = genai.Client(
            api_key=api_key,
            http_options={'api_version': 'v1'}
        )
        # 2. Usamos el modelo 2.5 que es el que tu cuenta tiene activo
        self.model_name = 'gemini-2.5-flash' 
        self.config = {
            "temperature": 0.45,       # Subimos un poco para que sea más analítico y fluido
            "top_p": 0.95,
            
        }
    @staticmethod
    def normalize_string(txt):
        # En Data Science, si no es string, devolvemos el valor original (ej. un nulo)
        if not isinstance(txt,str):
            return txt
        #Quitar espacios en los extremos y pasar a minúsculas
        textNormalize = txt.lower().strip()
        textNormalize = "".join(
            letra for letra in unicodedata.normalize('NFD',textNormalize)
            if unicodedata.category(letra) != 'Mn' 
            )
        
        return textNormalize
        
    def load_file(self, file):
        """Debe recibir un objeto de archivo (el que te da Streamlit), detectar si es .csv o .xlsx y devolver un DataFrame."""
       
        try:
            # Usamos .name porque Streamlit pasa un objeto de archivo
            nombre_archivo = file.name if hasattr(file,'name') else file
           
            if nombre_archivo.endswith('.csv'):
                dataFrame = pd.read_csv(file)
                # print(dataFrame)
                return dataFrame
            
            elif nombre_archivo.endswith('.xlsx'):
                
                dataFrame = pd.read_excel(file)
                # print(dataFrame)
                return dataFrame
            else:
                return None 
        except Exception as e:
            print(f"Algo salio mal {e}")
            return None
            
    def load_sql(_self,url,consultaSQL="SELECT * FROM ventas"):
        """Debe recibir la URL de conexión y un String con la consulta SQL. Debe usar create_engine de sqlalchemy para traer los datos."""
        
        #El parámetro _self (con guion bajo) le dice a Streamlit que no intente cachear la clase entera, solo los datos del DataFrame.
        try:
            # 1. LIMPIEZA DE RUTA: Si es un archivo local .db y no tiene el protocolo, se lo agregamos
            if url.endswith('.db') and not url.startswith('sqlite:///'):
                # Reemplazamos \ por / para evitar errores de escape en Windows
                url_limpia = url.replace('\\', '/')
                url = f"sqlite:///{url_limpia}"
                
            #creando el motor engine de conexion
            engine = create_engine(url, echo=True)## echo=True para ver queriesen consola
                
            # Pandas se encarga de conectar, ejecutar la query y cerrar laconexión solo, esta vez lo hacemos con pandas y no solo con createengine, pero abajo te detallo  mas de esa funcion muy interesante
            df = pd.read_sql(consultaSQL, engine)
            
            # Validación de seguridad: ¿Trajo datos?
            if df.empty:
                raise ValueError("La consulta se ejecutó pero la tabla está vacía.")
                
            return df
            
            
        except Exception as e:
            # 4. MANEJO DE ERRORES ESPECÍFICOS
            error_msg = str(e)
            if "nosuchtable" in error_msg.lower():
                raise Exception("❌ Error: La tabla especificada no existe en la base de datos.")
            elif "could not open database" in error_msg.lower():
                raise Exception("❌ Error: No se encontró el archivo .db. Verifica la ruta.")
            else:
                raise Exception(f"❌ Error de Conexión: {error_msg}")
    
    def run_audit(self, df, col_fecha):
        """Versión avanzada con Log de Auditoría Visual."""
        log = []
        # 1. Normalización de Textos
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].apply(self.normalize_string)
            
        # 2. Duplicados
        dupes = df.duplicated().sum()
        df = df.drop_duplicates().reset_index(drop=True)
        if dupes > 0: log.append(f"✨ Se eliminaron {dupes} filas duplicadas.")

        # 3. Fechas
        df[col_fecha] = pd.to_datetime(df[col_fecha], errors='coerce')
        nat_count = df[col_fecha].isna().sum()
        df = df.dropna(subset=[col_fecha])
        if nat_count > 0: log.append(f"📅 Se corrigieron {nat_count} fechas con formato inválido.")
        
        if not df.empty:
            df[col_fecha] = df[col_fecha].dt.normalize()
        else:
            raise ValueError("La columna no contiene fechas válidas.")

        # 4. Nulos en otras columnas
        for col in df:
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(0)
            else:
                df[col] = df[col].fillna('n/a')
        
        return df, log # Devolvemos el DataFrame y la lista de cambios
    
    def calculate_temporal_growth(self,df,col_fecha, col_valor):
        
        """
        Detecta y normaliza fechas en todas las columnas de tipo string de un DataFrame.
        """
        try:
            # 1. Copiamos el DF para no destruir el original (Inmutabilidad)
            temp_df = df.copy()

            # 2. Tu lógica de limpieza aplicada solo a la columna que el usuario eligió
            # Usamos errors='coerce' para que lo que NO es fecha sea NaT (Not a Time)
            temp_df[col_fecha] = pd.to_datetime(temp_df[col_fecha], errors='coerce')
            
            # Limpiamos la columna de dinero (col_valor)
            temp_df[col_valor] = pd.to_numeric(temp_df[col_valor], errors='coerce').fillna(0)

            # 3. Quitamos filas donde la fecha falló
            temp_df = temp_df.dropna(subset=[col_fecha])

            # 4. Resampling (Agrupación por mes)
            # Seteamos el índice solo para el cálculo
            ventas_por_mes = temp_df.set_index(col_fecha).resample('ME')[col_valor].sum()

            # 5. EL TRUCO DEL 0.0 (Validación de longitud)
            if len(ventas_por_mes) < 2:
                print("Advertencia: Datos insuficientes para comparar meses.")
                return 0.0

            # 6. Cálculo con iloc
            ultima = ventas_por_mes.iloc[-1]
            penultima = ventas_por_mes.iloc[-2]

            if penultima < 1: return 0.0 # Evita división por cero
            
            crecimiento = ((ultima - penultima) / penultima) * 100
            #print(temp_df)
            return float(crecimiento)

        except Exception as e:
            print(f"Error en análisis temporal: {e}")
            return 0.0
        
    def get_pareto_analysis(self, df, group_col, value_col):
        """Pareto es un algoritmo de Segmentación (clasifica qué es importante y qué no)."""
        #en esta funcion nosotros encontramos el producto mas importante
        try:
            # Validación preventiva: ¿Hay datos?(linea agregada para control de errores)
            if df.empty or group_col not in df.columns or value_col not in df.columns:
                return pd.DataFrame() # Devolvemos un DF vacío en lugar de None
            
            #agrupamos por las columna que elija, sumamos y reseteamos el indice, luego ordenamos de forma decendiente
            df_pareto = df.groupby(group_col)[value_col].sum().reset_index()
            df_pareto = df_pareto.sort_values(by=value_col,ascending= False)
            
            total = df_pareto[value_col].sum()
            if total == 0: return df_pareto # Evita división por cero (linea agregada para control de errores)
            
            #creamos una nueva columna y calculamos la el acumulado de la columna de valor
            df_pareto['acumulado'] = df_pareto[value_col].cumsum()
            print(f"acumulado: {df_pareto['acumulado']}")
            
            #Calculamos el porcentaje acumulado sobre el total general
            total_acumulado = df_pareto[value_col].sum()
            print(f"total_acumulado: {total_acumulado}")
            df_pareto['porcentaje_acumulado'] = (df_pareto['acumulado'] / total_acumulado) * 100
            
            #encontramos el producto que representa el 80% de las ventas
            mayor_consumo = df_pareto[df_pareto['porcentaje_acumulado'] <= 85]
            print(f"Analisis de los 80%: {mayor_consumo}")
                
            return df_pareto
        except Exception as e:
            print(f"Error en Pareto: {e}")
            return None
    
    def redict_next_month(self, df, col_fecha, col_valor):
        #recibimos dos argumentos
        #1: fecha, que sera la columna fecha que nos indique el susuario
        #2: el valor a analizar puede ser ventas, cantidades etc
        try:
            dataFrame = df.copy()
            #Con pandas convertimos el tipo de dato fecha de string a date
            dataFrame[col_fecha] = pd.to_datetime(dataFrame[col_fecha], errors='coerce')
            
            #Aca agrupamos por messacamos el valor por mes 
            serieMensual = dataFrame.set_index(col_fecha).resample('ME')[col_valor].sum().fillna(0)
            
            #Preparar X (tiempo) e Y (ventas)
            
            # y = los valores de ventas [100, 200, 300]
            y = serieMensual.values
            # x = los índices de tiempo [0, 1, 2] según cuántos meses hay
            x = np.arange(len(y))
            
            # np.polyfit encuentra la pendiente (m) y la ordenada (b)
            if len(y) < 2:
                print('No hay suficiente informacion para predecir una tendencia')
                return 0.0
            # Retorna [m, b]
            modelo_IA_Mio = np.polyfit(x, y, 1) #orden ej: (x,y,1)
            
            # Creamos la función matemática
            funcion_predictiva = np.poly1d(modelo_IA_Mio)
            
            #Predecir el futuro
            # Si hoy estamos en el índice 'n', el mes que viene es 'n+1'
            indice_mes_proximo = len(y)
            
            #Prediccion del mes siguiente de tus ventas o lo que sea
            prediccion = funcion_predictiva(indice_mes_proximo)
            
            return max(0.0, float(prediccion))
        except Exception as e:
            print(f"Ocurrio un error en nuestro machineLearning: {e}")
            return 0.0
           
    def get_ai_insight_prompt(self, valor_actual, prediccion, vips, perfil_negocio, ubicacion="", idioma="Español"):
        try:
            # 1. BLINDAJE DE DATOS (Tu estándar de seguridad)
            v_actual = float(valor_actual) if valor_actual is not None else 0.0
            v_pred = float(prediccion) if prediccion is not None else 0.0
            variacion = ((v_pred - v_actual) / v_actual) * 100 if v_actual != 0 else 0
            
            estado_es = "crecimiento" if variacion > 0 else "baja"
            estado_en = "growth" if variacion > 0 else "decline"
            lista_vips = ", ".join([str(item) for item in vips]) if vips else "No identificados / Not identified"
            
            # 2. LÓGICA MULTILINGÜE Y GEOGRÁFICA
            if idioma == "English":
                contexto_geo = f"in {ubicacion}" if ubicacion and ubicacion.strip() != "" else "in the global market"
                instruccion_geo = f"specifically for the reality of {ubicacion}" if ubicacion else "based on international best practices"
                
                prompt = f"""
                SYSTEM INSTRUCTION: RESPOND ONLY IN ENGLISH.
                ROLE: SENIOR BUSINESS CONSULTANT & FINANCIAL STRATEGIST.
                
                CONTEXT:
                - Industry: {perfil_negocio}
                - Market: {contexto_geo}
                - Current Month Sales: ${v_actual:,.2f}
                - Next Month Forecast: ${v_pred:,.2f}
                - Trend: {estado_en} of {abs(variacion):,.2f}%
                - Star Products: {lista_vips}

                TASK: Provide 3 strategic pillars to dominate the market:
                1. 🎯 SCALABILITY: How to boost star products in the {perfil_negocio} sector.
                2. 📍 MARKET STRATEGY: A marketing tactic {instruccion_geo}.
                3. 🚀 COMPETITIVE ADVANTAGE: How to outperform competitors and increase average ticket.

                REQUIREMENTS: Bold, professional tone, with emojis and actionable steps. RESPOND IN ENGLISH.
                """
            else:
                contexto_geo = f"en {ubicacion}" if ubicacion and ubicacion.strip() != "" else "en el mercado global"
                instruccion_geo = f"específicamente para la realidad de {ubicacion}" if ubicacion else "basada en las mejores prácticas de su sector a nivel internacional"

                prompt = f"""
                INSTRUCCIÓN DE SISTEMA: RESPONDE ÚNICAMENTE EN ESPAÑOL.
                ROL: SENIOR BUSINESS CONSULTANT & ESTRATEGA FINANCIERO.
                
                CONTEXTO:
                - Rubro: {perfil_negocio}
                - Mercado: {contexto_geo}
                - Ventas mes actual: ${v_actual:,.2f}
                - Predicción mes próximo: ${v_pred:,.2f}
                - Tendencia: {estado_es} del {abs(variacion):,.2f}%
                - Productos Estrella: {lista_vips}

                TAREA: Proporciona 3 pilares estratégicos para dominar el mercado:
                1. 🎯 ESCALABILIDAD: Cómo potenciar los productos estrella en el rubro {perfil_negocio}.
                2. 📍 ESTRATEGIA DE MERCADO: Una táctica de marketing {instruccion_geo}.
                3. 🚀 VENTAJA COMPETITIVA: Cómo superar a la competencia y aumentar el ticket promedio.

                REQUERIMIENTOS: Tono audaz, profesional, con emojis y pasos accionables. RESPONDER EN ESPAÑOL.
                """
            return prompt
        except Exception as e:
            return f"Error al preparar consultoría: {e}"  
     
    def get_ai_analysis(self, prompt):
        """
        Llamada optimizada. Soluciona el error 404 forzando versiones estables
        y maneja la cuota de forma profesional.
        """
        if not self.client:
            return "🔧 **ProfitLens AI:** Motor no configurado."

        try:
            # INTENTO 1: Modelo estándar estable (v1)
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=self.config
            )
            return response.text
            
        except Exception as e:
            err = str(e).lower()
            
            # SOLUCIÓN AL 404: Reintento con versión de producción específica
            if "404" in err or "not found" in err:
                try:
                    # Forzamos la versión flash-002 (estándar de producción 2026)
                    res = self.client.models.generate_content(
                        model='gemini-1.5-flash-002',
                        contents=prompt,
                        config=self.config
                    )
                    return res.text
                except:
                    # ÚLTIMO RECURSO: Gemini 1.5 Pro (más lento pero infalible en facturación)
                    try:
                        res = self.client.models.generate_content(model='gemini-1.5-pro', contents=prompt)
                        return res.text
                    except:
                        return "🌐 **Error de Modelo:** No se encontró una versión disponible. Verifica tu habilitación de API en Google Cloud."

            if "429" in err or "quota" in err:
                return "⚠️ **Capacidad Alcanzada:** Esperá 60 segundos para refrescar la cuota."
            
            if "400" in err or "api_key_invalid" in err:
                return "🔑 **Error de Clave:** La API Key es inválida o el proyecto no tiene habilitada la Generative Language API."

            return f"🌐 **Error de Conexión:** {str(e)[:100]}"




"""normalize_string()
EXPLICACIONES:

Método Estático (@staticmethod): Como la normalización es una utilidad que podrías querer usar sin necesidad de crear todo un objeto "Engine" (por ejemplo, para limpiar un solo texto suelto), la declaramos estática.

# normalize_string()
# Desglose paso a paso
#     unicodedata.normalize('NFD', texto)
    # Resultado: 'canción'  (la ó se convierte en 'o' + '◌́')
    
#     Usa el módulo unicodedata para normalizar el texto en forma NFD (Normalization Form Decomposition).
#     Esto descompone los caracteres acentuados en:
#     La letra base (por ejemplo "á" → "a")
#     El acento como un carácter separado (marca diacrítica).  
#     for c in ...

#     Recorre cada carácter resultante de la normalización.
#     unicodedata.category(c)

#     Devuelve la categoría Unicode del carácter c.
#     "Mn" significa Mark, Nonspacing (marca no espaciadora), que son los   acentos y otros signos que se colocan sobre o debajo de las letras.
#     if unicodedata.category(c) != 'Mn'

#     Filtra y descarta los caracteres que sean marcas diacríticas (Mn).
#     Así, se eliminan los acentos y se conservan solo las letras base.
#     "".join(...)

#     Une todos los caracteres filtrados en una nueva cadena sin acentos.      
        
        """
        
"""load_sql():
EXPLICACIONES y ejemplos de como usar create_engine


# Crear un motor (engine) para la base de datos SQLite en memoria
engine = create_engine('sqlite:///:memory:', echo=True) # echo=True para ver queries en consola

# Crear una conexión
with engine.connect() as connection:
    # Crear una tabla de ejemplo
    connection.execute(text('''
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            edad INTEGER
        )
    '''))
    
    # Insertar registros en la tabla
    connection.execute(text("INSERT INTO usuarios (nombre, edad) VALUES (:nombre, :edad)"),
                       [{"nombre": "Juan", "edad": 25},
                        {"nombre": "María", "edad": 30},
                        {"nombre": "Ana", "edad": 28}])
    
    # Realizar una consulta SELECT
    result = connection.execute(text("SELECT * FROM usuarios WHERE edad > :edad_min"), {"edad_min": 26})
    
    # Mostrar resultados
    for fila in result:
        print(f"ID: {fila.id}, Nombre: {fila.nombre}, Edad: {fila.edad}")

"""

"""get_pareto_analysis

EXPLICACION!!!!!!!!!!!!

1. ¿Qué es el groupby y qué se suma?
Imaginá que tu Excel tiene 10 filas de "Smartphone X" a $500 cada una.

groupby('producto'): Junta todas las filas que digan "Smartphone X" en un solo grupito.

['precio_unitario'].sum(): Entra a ese grupito y suma todos los precios.

Resultado: Pasás de tener 10 filas de $500 a 1 sola fila de $5.000.

2. ¿Por qué usamos reset_index()?
Cuando hacés un groupby, la columna por la que agrupaste ("producto") deja de ser una columna normal y se convierte en el índice (el nombre de la fila).

Si no hacés reset_index(), no podés usar df['producto'] después porque para Pandas ya no es una columna.

reset_index() "baja" al nombre de la fila y lo vuelve a convertir en una columna común y corriente.

3. Diferencia entre sum() y cumsum()
Esta es la clave de la Ciencia de Datos:

sum() (Suma Total): Es un solo número. La suma de TODAS las ventas de la empresa (ej: $10.000).

cumsum() (Suma Acumulada): Es una lista que crece.

Fila 1: $5.000

Fila 2: $5.000 + $3.000 = $8.000

Fila 3: $8.000 + $1.000 = $9.000

Esto nos sirve para ver en qué momento llegamos a cubrir el 80% del total.

"""

"""Concepto de Ciencia de Datos:

1. duplicated().sum(): Cuenta filas idénticas. 
2. isnull().sum().sum(): Cuenta cuántos "huecos" hay en todo el dataset.
3. select_dtypes: Es la forma profesional de separar columnas de dinero/cantidades de las de nombres/categorías.
"""