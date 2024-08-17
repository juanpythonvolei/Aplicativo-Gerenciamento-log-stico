import pathlib
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
import requests
import streamlit as st
import os


def ia(pergunta):
    
    GOOGLE_API_KEY = st.secrets['firebase']['GOOGLE_API_KEY']
    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel('gemini-1.5-flash')

    chat = model.start_chat(history=[])
    requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
    roteiro = requiscao.json()
    dados = roteiro['bancodedadosroteirooficial']
    texto_nota = ''
    for item in dados:
            roteiro = dados[f'{item}']
            for elemento in roteiro:
                    nota = roteiro[f'{elemento}']
                    numero_nota = nota['Número da Nota']
                    destino = nota['Destino']
                    data_De_emissao = nota['Data de Emissão']
                    volumes = nota['Volumes']
                    cliente = nota['Cliente']
                    Produtos = nota['Produtos'][0]
                    status = nota['status']
                    valor  = nota['Valor Total']
                    infos = f'Numero nota:{numero_nota}. volumes:{volumes}. cliente:{cliente}. Produtos:{Produtos}. status:{status}. valor:{valor}. destino:{destino}. data de emissão:{data_De_emissao}\n'
                    texto_nota += str(infos)
    response = chat.send_message(f'Você está vizualiando conjuntos de informações relacionados a notas fiscais. Então, responda ao que for solicitado.{pergunta}:\n\n{texto_nota}\n')
    resposta = response.text
    st.info(f'{resposta}')

