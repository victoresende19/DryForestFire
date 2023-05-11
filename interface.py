import pandas as pd
import numpy as np

import base64
import streamlit as st

import joblib
from tensorflow.keras.models import load_model

from utils.plots import line_plot
from utils.style import set_background


df = pd.read_csv('Data/inmet_inpe.csv')
df = df.rename(columns={'Data Medicao': 'Data Medição',
                        'frequencia_incendios': 'Frequência de incêndios',
                        'PRECIPITACAO': 'Precipitação'})

rede_neural = load_model('Models/rede_neural.h5')
floresta_aleatoria = joblib.load('Models/floresta_aleatoria')
scaler = joblib.load('Models/padronizacao')

st.set_page_config(page_icon='🔥', page_title='TCC', layout='wide')
background_image_url = "https://mattbeardart.com/wp-content/uploads/2020/06/2020-4-19-Trial-by-Fire-2000x2000px.jpg"
set_background('Images/background-app.jpg')
st.markdown("<h1 style='text-align: center; color: white; text-shadow: 5px 5px 5px #000000; font-size: 42px'> 🍂 Previsão de incêndios no DF 🍂 </h1>",
            unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white;'> Por Victor Augusto Souza Resende </p>",
            unsafe_allow_html=True)
st.markdown("<hr style='height: 5px; color: white; background-color: white' >",
            unsafe_allow_html=True)
st.markdown("<p style='text-align: justify; color: white;'> A cidade de Brasília possui uma característica climática referente a seca e estiagem. Portanto, esse estudo tenta demonstrar o impacto da estiagem em relacao a quantidade de incêndios na respectiva localidade. Abaixo é possível verificar a série histórica dos incêndios no período de 1998 a 2022.  </p>",
            unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(line_plot(df, 'Data Medição', 'Frequência de incêndios',
                    'Frequência de incêndios em Brasília - 1998 a 2022', 'red'), use_container_width=True)
with col2:
    st.plotly_chart(line_plot(df, 'Data Medição', 'Precipitação',
                    'Frequência de precipitacao em Brasília - 1998 a 2022', '#1dace0'), use_container_width=True)
st.markdown("<h2 style='text-align: center; color: white;'> Previsões </h2>",
            unsafe_allow_html=True)


form = st.form(key='my_form')

precipitacao = form.slider(
    'Precipitação (em mm): ',
    min_value=float(df.Precipitação.min()),
    max_value=float(df.Precipitação.max()),
    value=float(233.0))

temp_max = form.slider(
    'Temperatura Máxima Mensal (em °C): ',
    min_value=float(df.TEMPERATURA_MAXIMA_MEDIA.min()),
    max_value=float(df.TEMPERATURA_MAXIMA_MEDIA.max()),
    value=float(26.60))

SPEI3 = form.slider(
    'SPEI3 (Índice que mede a severidade da seca. Quanto menor, mais seco. Quanto maior, mais úmido): ',
    min_value=float(df.SPEI3.min()),
    max_value=float(df.SPEI3.max()),
    value=float(1.357870))

months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
          "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
selected_month = form.radio('Selecione um mês', months, horizontal=True)
month_array = [int(selected_month == month) for month in months]

submit_button = form.form_submit_button(label='✨ Aplicar filtros')

value = np.array([precipitacao, SPEI3, temp_max] + month_array).reshape(-1, 15)

previsao_floresta = floresta_aleatoria.predict(scaler.transform(value))
previsao_rede = rede_neural.predict(scaler.transform(value))

col1, col2, col3 = st.columns(3)

with col1:
    st.write('')
with col2:
    st.markdown(f"""
                <p style='text-align: justify; color: black; font-size: 18px'> 
                    Previsão quantidade de incêndios com Random Forest: {previsao_floresta[0]:.0f} incêndios <br> Previsão quantidade de incêndios com Rede Neural: {previsao_rede[0][0]:.0f} incêndios
                </p>""",
                unsafe_allow_html=True)
with col3:
    st.write('')

