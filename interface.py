import pandas as pd
import numpy as np
import time

import base64
import streamlit as st

import joblib
from tensorflow.keras.models import load_model

from utils.plots import line_plot, bar_plot
from utils.style import set_background


df = pd.read_csv('Data/inmet_inpe.csv')
df = df.rename(columns={'Data Medicao': 'Data Medição',
                        'frequencia_incendios': 'Frequência de incêndios',
                        'PRECIPITACAO': 'Precipitação',
                        'mes': 'Mês'})

rede_neural = load_model('Models/rede_neural.h5')
floresta_aleatoria = joblib.load('Models/floresta_aleatoria')
scaler = joblib.load('Models/padronizacao')

st.set_page_config(page_icon='🔥', page_title='TCC', layout='wide')
background_image_url = "https://mattbeardart.com/wp-content/uploads/2020/06/2020-4-19-Trial-by-Fire-2000x2000px.jpg"
set_background('Images/background-app.jpg')
st.markdown("<h1 style='text-align: center; color: white; text-shadow: 5px 5px 5px #000000; font-size: 42px'> 🍂 Previsão de incêndios florestais no DF 🍂 </h1>",
            unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white;'> Por Victor Augusto Souza Resende </p>",
            unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white;'> Trabalho de conclusão de curso (IESB) - Bacharelado em ciência de dados e inteligência artificial </p>",
            unsafe_allow_html=True)
st.markdown("<hr style='height: 5px; color: white; background-color: white' >",
            unsafe_allow_html=True)

st.markdown("""
            <div class="container">
                <p style='text-align: justify; color: white; margin-left: 10px; font-size: 16px'> A estiagem em Brasília, Distrito Federal, traz consigo diversos impactos significativos. Durante os períodos de seca prolongada, os recursos hídricos da região sofrem consideravelmente, levando à diminuição dos níveis de água em rios, lagos e represas. Isso resulta em escassez de água para consumo humano, agrícola e industrial, além de afetar a biodiversidade local. A falta de chuvas também contribui para o aumento da poluição do ar, uma vez que a umidade reduzida dificulta a dispersão dos poluentes. Ademais, a estiagem agrava os problemas relacionados à saúde, como doenças respiratórias e o surgimento de incêndios florestais, colocando em risco a qualidade de vida da população e o equilíbrio dos ecossistemas locais.  </p>  
                <p style='text-align: justify; color: white; margin-right: 10px; font-size: 16px'> A diminuição da umidade do ar e a falta de chuvas tornam a vegetação mais suscetível à propagação do fogo, transformando áreas verdes em verdadeiras fontes de combustível. Além disso, a escassez de água dificulta o combate aos incêndios, tornando-os mais desafiadores de controlar. Os incêndios florestais causam danos significativos ao meio ambiente, resultando na perda de biodiversidade, destruição de habitats naturais e emissão de grandes quantidades de gases de efeito estufa, contribuindo para as mudanças climáticas. Portanto, essa aplicação tem o objetivo de tornar pública a interação de usuários com os modelos preditivos desenvolvidos visando a predição da quantidade de queimadas por variáveis climáticas, do quail pode-se acessar a documentação do estudo <a href='https://github.com/victoresende19/DryForestFire'>clicando aqui</a>  </p>
            </div>
            """,
            unsafe_allow_html=True)

st.markdown("<hr style='height: 5px; color: white; background-color: white' >",
            unsafe_allow_html=True)


st.markdown("<h2 style='text-align: center; color: white;'> Visualização das séries históricas </h2>",
            unsafe_allow_html=True)

st.markdown("""
            <div class="container">
                <p style='text-align: justify; color: white; font-size: 16px; margin-left: 10px'> A fim de demonstrar a distribuição da quantidade de incêndios pelos anos, decidiu-se pelas breves visualizações abaixo, das quais estão analisadas e melhores detalhadas na pesquisa escrita. Entretanto, no primeiro gráfico é possível identificar anos dos quais houveram fortes picos de queimadas.  </p>  
                <p style='text-align: justify; color: white; font-size: 16px; margin-right: 10px'> Da mesma forma, o segundo gráfico revela a agregação mensal das frequências de incêndios florestais, evidenciando que os meses com maior incidência estão relacionados ao período de seca em Brasília, quando a cidade atinge seu pico de escassez de chuvas. </p>
            </div>
            """,
            unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(line_plot(df, 'Data Medição', 'Frequência de incêndios',
                    'Frequência de incêndios em Brasília - 1998 a 2022', 'red'), use_container_width=True)
with col2:
    st.plotly_chart(bar_plot(df.groupby('Mês', sort=False).sum('Frequência de incêndios').reset_index(), 'Mês', 'Frequência de incêndios',
                    'Quantidade de incêndios por mês em Brasília - 1998 a 2022', 'Frequência de incêndios', 'oranges'), use_container_width=True)
st.markdown("<h2 style='text-align: center; color: white;'> Previsões dos modelos de Random Forest e Rede Neural</h2>",
            unsafe_allow_html=True)
st.markdown("<p style='text-align: justify; color: white; font-size: 16px;'> Como citado no estudo, decidiu-se pela aplicação dos dois melhores modelos preditivos: random forest e a arquitetura rede neural, através das variáveis precipitação, temperatura máxima, SPEI3 e o mês desejado. Vale ressaltar que os modelos foram treinados com 24 anos de dados referente ao território de Brasília. Para mais informações dos modelos, como as métricas e criação, acessar a documentação referida no início da página.</p>",
            unsafe_allow_html=True)


form = st.form(key='my_form')

precipitacao = form.slider(
    'Precipitação prevista (em mm): ',
    min_value=float(df.Precipitação.min()),
    max_value=float(df.Precipitação.max()),
    value=float(233.0))

temp_max = form.slider(
    'Temperatura Máxima Mensal prevista (em °C): ',
    min_value=float(df.TEMPERATURA_MAXIMA_MEDIA.min()),
    max_value=float(df.TEMPERATURA_MAXIMA_MEDIA.max()),
    value=float(26.60))

SPEI3 = form.slider(
    'SPEI3 (Índice que mede a severidade da seca. Quanto menor, mais seco. Quanto maior, mais úmido) previsto: ',
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
    with st.spinner("Fazendo previsão..."):
        time.sleep(1)
        st.markdown(f"""
                <p style='text-align: justify; color: black; font-size: 20px'> 
                    Previsão quantidade de incêndios com Random Forest: {previsao_floresta[0]:.0f} incêndios <br> Previsão quantidade de incêndios com Rede Neural: {previsao_rede[0][0]:.0f} incêndios
                </p>""",
                unsafe_allow_html=True)
with col3:
    st.write('')

