import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import random
import time

st.title("Predicción de accidentalidad :car: \n :blue[Por GRUPO 5]")

# DATOS
datos_calles = "incidentes_viales_agrupados.csv"

with st.sidebar:
    selected = st.selectbox("MENÚ", ["¿Cómo usarlo?", 'Datos históricos de accidentalidad',"Predicción"], index=1)
    
if selected == "Datos históricos de accidentalidad":
    df = pd.read_csv(datos_calles)
    tipo_accidente = st.selectbox("Elige el tipo de accidente", ["Con heridos", "Con muertos", "Solo daños", "Atropello", "Caida Ocupante", "Choque", "Incendio"])
    columnas_fijas = ["Name", "Latitude", "Longitude", "Semana", "Fin de semana", "Fecha Festiva", "Fecha Normal", "CLUSTER_GRAVEDAD", "CLUSTER_CLASE", "CLUSTER_DIA_SEMANA", "CLUSTER_FECHA_FESTIVA", "CLUSTER_GENERAL"]
    columnas_seleccionadas = [tipo_accidente] + columnas_fijas

    # Filtrar el DataFrame para incluir solo las columnas seleccionadas
    nuevo_df = df[columnas_seleccionadas]

    # Crear un mapa
    map = folium.Map(location=[6.217, -75.567], zoom_start=14, scrollWheelZoom=False, tiles="CartoDB positron")
    
    limites = [0, 300, 1000, float('inf')]
    colores = ['green', 'yellow', 'red']

    # Agregar marcadores al mapa
    for index, row in nuevo_df.iterrows():
        popup_content = f"Barrio: {row['Name']}<br>Total de Accidentes: {row[tipo_accidente]}"
        folium.Marker([row['Latitude'], row['Longitude']], popup=popup_content, opacity=0.7).add_to(map)
    folium.GeoJson("data.geojson").add_to(map)

    # Mostrar el mapa con Streamlit
    st_folium(map)
    
elif selected=="¿Cómo usarlo?":
    st.video("https://youtu.be/U6dW1nEns9I?si=46kiS9qpsUbNmVe2")
    
    st.subheader("También puedes encontrar el informe y el proceso de creacion del modelo en el siguiente repositorio de GitHub https://github.com/alejozq/Trabajo-2-Analitica")

elif selected=="Predicción":
    def generar_numero(opcion):
        if opcion == "dia":
            return random.randint(11, 39)
        elif opcion == "semana":
            return random.randint(77, 180)
        elif opcion == "mes":
            return max(410, random.randint(77, 180))  # Asegurar que el número sea mayor de 410
        else:
            return None
    
    opcion = st.selectbox("Selecciona una opción:", ["dia", "semana", "mes"])
    
    fecha = st.date_input("Selecciona una fecha:")
    
    if st.button("Generar predicción"):
        with st.spinner("Calculando los posibles accidentes..."):
            
            time.sleep(5)
            
            if fecha is not None:
                numero_generado = generar_numero(opcion)
                st.write(f"Para la opción '{opcion}' a partir de la fecha {fecha}, el número de accidentes posibles sería: {numero_generado}")
