# STREAMLIT

import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
# Cargar el modelo
with open('../models/Modelo_prediccion_EnergyDelta_RandomForestRegressor.sav', 'rb') as file:
    model = pickle.load(file)
# Personalizar el estilo
st.markdown("""
    <style>
    body {
        background-color: #E0F7E0; /* Color verde claro */
    }
    .main {
        background-image: url('https://www.solidbackgrounds.com/images/2560x1600/2560x1600-light-green-solid-color-background.jpg');
        background-size: cover;
        background-position: center;
    }
    h1 {
        color: #4CAF50;
        text-align: center;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
    }
    .stSlider {
        color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)
# Título del sitio
st.title("Calculador Energía Delta (Wh) :")
# División en columnas
col1, col2 = st.columns(2)
# Configuración de sliders en columna 1
with col1:
    hour = st.slider('Introduce la hora:', 0, 24, step=1)
    GHI = st.slider('Introduce la GHI (W/m2):', 1, 250, step=1)
    temp = st.slider('Introduce la temperatura (Cº):', -15, 50, step=1)
    pressure = st.slider('Presión atmosférica (mbar):', 950, 1050, step=10)
    humidity = st.slider('Introduce la humedad %:', 0, 100, step=1)
    wind_speed = st.slider('Introduce la velocidad de viento (m/s):', 0, 30, step=1)
# Configuración de sliders en columna 2
with col2:
    rain_1h = st.slider('Introduce la cantidad de lluvia (l/m2):', 0, 10, step=1)
    snow_1h = st.slider('Introduce la cantidad de nieve (l/m2):', 0, 10, step=1)
    clouds_all = st.slider('Introduce las nubes (%):', 0, 100, step=1)
    sunlightTime = st.slider('Introduce la duración del tiempo solar (minutos):', 20, 1020, step=1)
    dayLength = st.slider('Introduce el tiempo total del día (minutos):', 450, 1000, step=1)
    SunlightTimedaylength = st.slider('Introduce la SunlightTime/daylength (minutos):', 0.1, 1.0, step=0.01)
# Selectboxes
month = st.selectbox('Mes:', ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'])
weather_type_n = st.selectbox('Tiempo meteorológico:', ['Despejado', 'Ligeramente Nublado', 'Nublado', 'Muy Nublado', 'Tormentoso'])
isSun_n = st.selectbox('¿Hay sol?', ['Yes', 'No'])
# Botón de predicción
if st.button("Predict"):
    month_mapping = {'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12}
    weather_type_n_mapping = {'Despejado': 1, 'Ligeramente Nublado': 2, 'Nublado': 3, 'Muy Nublado': 4, 'Tormentoso': 5}
    isSun_n_mapping = {'Yes': 1, 'No': 0}
    row = [
        month_mapping[month],
        hour,
        GHI,
        temp,
        pressure,
        humidity,
        wind_speed,
        rain_1h,
        snow_1h,
        clouds_all,
        sunlightTime,
        dayLength,
        SunlightTimedaylength,
        weather_type_n_mapping[weather_type_n],
        isSun_n_mapping[isSun_n]
    ]
    y_pred = model.predict([row])
    st.write(f'La energía recogida con estas circunstancias meteorológicas: {y_pred[0]:,.2f}Wh')
    # Visualización de resultados
    fig, ax = plt.subplots()
    ax.bar(['Predicción'], [y_pred[0]], color='#4CAF50')
    ax.bar(['Registro bajo'], [200], color='blue')
    ax.bar(['Registro alto'], [2000], color='red')
    ax.set_ylabel('Energía (Wh)')
    ax.set_ylim(0, 3000)
    ax.set_title('Predicción de Energía')
    st.pyplot(fig)
    # Agregar una imagen relevante
    st.image("https://elperiodicodelaenergia.com/wp-content/uploads/2019/03/Planta-fotovoltaica-Don-Rodrigo-de-BayWa-re..jpg", caption="Solar Panels", use_column_width=True)