import base64
import streamlit as st


def set_background(png_file: str):
    """
    Description
    -----------
    Faz a leitura do arquivo de imagem de maneira binária (rb).

    Parameters
    ----------
    png_file: str
        Caminho do arquivo imagem.

    Returns
    -------
    Retorna a imagem traduzida/decodificada de forma binária alterando o css do app streamlit.
    """

    with open(png_file, 'rb') as f:
        data = f.read()

    bin_str = base64.b64encode(data).decode()
    page_bg_img = '''
        <style>
            .stApp {
                background-image: url("data:image/png;base64,%s");
                background-size: cover;
            }
            .css-ocqkz7, .e1tzin5v4, css-12ttj6m, .epcbefy1 {
                background-color: #F8F8FF;
                border: 2px solid black;
            }
            .css-184tjsw, .e16nr0p34{
                color: black
            }
        </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
