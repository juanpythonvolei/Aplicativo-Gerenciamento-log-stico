import streamlit as st
import requests
import re
from pathlib import Path 
from datetime import datetime
import xmltodict
import shutil
import datetime
import requests
import firebase_admin
from firebase_admin import credentials, firestore,db
from time import sleep
import pprint
from st_circular_progress import CircularProgress
import webbrowser
from suporte_inteligente import ia
from streamlit_option_menu import option_menu
import time
@st.dialog(f"Deseja realmente acessar a rota da nota?") 
def escolha():    
                                                            
                                                            sim = st.button('Sim')
                                                            if sim:
                                                                    lista = [] 
                                                                    destinos_info = []
                                                                    requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
                                                                    roteiro = requiscao.json()
                                                                    dados = roteiro['bancodedadosroteirooficial']
                                                                    for item in dados:
                                                                      if item != 'Comprovantes':
                                                                            roteiro = dados[f'{item}']
                                                                            for elemento in roteiro:
                                                                                nota = roteiro[f'{elemento}']
                                                                                if nota['Número da Nota'] == str(pesquisa_nota):
                                                                                    numero = nota['Número da Nota']
                                                                                    volumes = nota['Volumes']
                                                                                    valor = nota['Valor Total']
                                                                                    Cliente  = nota['Cliente']
                                                                    address = "Itupeva,sp"
                                                                    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
                                                                    params = {
                                                                                                "address": address,
                                                                                                "key": st.secrets['firebase']['chave_api_googlemaps']  # Substitua pela sua chave de API
                                                                                            }
                                                            
                                                                    response = requests.get(base_url, params=params)
                                                                    data = response.json()
                                                                    if data["status"] == "OK":
                                                                                                location = data["results"][0]["geometry"]["location"]
                                                                                                lat_inicial = location["lat"]
                                                                                                lon_inicial = location["lng"]
                                                                    ponto_partida = (lat_inicial, lon_inicial)
                                                                    ponto_partida_dict = {
                                                                                        'destino': 'Itupeva, SP',
                                                                                        'distancia': 0,
                                                                                        'Número da nota': '',
                                                                                        'volumes': '',
                                                                                        'Duração': '',
                                                                                        'coordenadas': ponto_partida,
                                                                                        'coordenadas_google': f'{lat_inicial},{lon_inicial}',
                                                                                        'cliente': ''
                                                                                    }
                                                                    destinos_info.append(ponto_partida_dict['coordenadas_google'])
                                                                    destino = nota['Destino']
                                                                                    
                                                                    address = f"{destino}"
                                                                    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
                                                                    params = {
                                                                                                "address": address,
                                                                                                "key": st.secrets['firebase']['chave_api_googlemaps']  # Substitua pela sua chave de API
                                                                                            }
                                                            
                                                                    response = requests.get(base_url, params=params)
                                                                    data = response.json()
                                                                    if data["status"] == "OK":
                                                                                                location = data["results"][0]["geometry"]["location"]
                                                                                                lat_final = location["lat"]
                                                                                                lon_final = location["lng"]
                                                                                                localizacao = f'{lat_final},{lon_final}'
                                                                                                destinos_info.append(localizacao)
                                                                    final = base_url2 + '/'.join(destinos_info)
                                                                    link  = st.link_button("Acessar Rota",final)     
                                                                    st.info(f'Nota: {numero} volumes: {volumes} valor:{valor} cliente:{Cliente}')
                                                            else:    
                                                                    st.info(f'Você ainda não acessou a rota da nota')
css = """                                                    
<style>
.centered-image {
    display: block;
    margin: 0 auto;
}
</style>
"""

# Insere o CSS no aplicativo
st.markdown(css, unsafe_allow_html=True)

# Exibe a imagem centralizada
image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
seletor  = option_menu("Menu Principal", ["rota da nota", "rota de todas as notas","suporte inteligente"], icons=["truck", "map",'robot'],menu_icon=['menu-button-wide-fill'])


lista_a = []
base_url2 = "https://www.google.com/maps/dir/"
if seletor == 'rota da nota':
        time.sleep(0.5)
        msg1 = st.toast('Seja Bem vindo (a)')
        time.sleep(0.5)
        msg2 = st.toast('Nessa seção, você pode ver a rota de uma nota específica ')
        requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
        roteiro = requiscao.json()
        try:
            dados = roteiro['bancodedadosroteirooficial']
            for item in dados:
                            if item != 'Comprovantes':
                              roteiro = dados[f'{item}']
                              for elemento in roteiro:
                                  nota = roteiro[f'{elemento}']
                                  numero = nota['Número da Nota']
                                  if numero in lista_a:
                                      pass
                                  else:
                                      lista_a.append(numero)
              pesquisa_nota = st.selectbox('',lista_a,index=None,placeholder='Selecione uma nota')
              if pesquisa_nota:
                     escolha()
        except:
            st.error('Sem Roteiros Disponíveis')
elif seletor == "rota de todas as notas":
        time.sleep(0.5)
        msg1 = st.toast('Seja Bem vindo (a)')
        time.sleep(0.5)
        msg2 = st.toast('Nessa seção, você pode ver a rota de todas as notas em função da data de emissão ')
        lista_total = []
        destinos_info = []
        requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
        roteiro = requiscao.json()
        try:
                                                                  dados = roteiro['bancodedadosroteirooficial']
                                                                  base_url2 = "https://www.google.com/maps/dir/"
                                                                  
                                                                  for item in dados:
                                                                          if item != 'Comprovantes':
                                                                            roteiro = dados[f'{item}']
                                                                            lista_total.append(item)
                                                                  opcao_selecionada = st.selectbox("", lista_total,index=None,placeholder='Selecione uma data')
                                                                  if opcao_selecionada:
                                                                    total = st.button("Pesquisar todas as rotas")
                                                                    if total:
                                                                        st.info(f'Total de Roteiros disponíveis: {len(lista_total)}')
                                                                        for item in dados:
                                                                          if item != 'Comprovantes':
                                                                            if item == opcao_selecionada:
                                                                                roteiro = dados[f'{item}']
                                                                                for elemento in roteiro:
                                                                                        nota = roteiro[f'{elemento}']
                                                                                        volumes = nota['Volumes']
                                                                                        valor = nota['Valor Total']
                                                                                        Cliente  = nota['Cliente']
                                                                                        
                                                                                        address = "Itupeva,sp"
                                                                                        base_url = "https://maps.googleapis.com/maps/api/geocode/json"
                                                                                        params = {
                                                                                                        "address": address,
                                                                                                        "key": st.secrets['firebase']['chave_api_googlemaps']  # Substitua pela sua chave de API
                                                                                                    }
                                                            
                                                                                        response = requests.get(base_url, params=params)
                                                                                        data = response.json()
                                                                                        if data["status"] == "OK":
                                                                                                        location = data["results"][0]["geometry"]["location"]
                                                                                                        lat_inicial = location["lat"]
                                                                                                        lon_inicial = location["lng"]
                                                                                                        ponto_partida = (lat_inicial, lon_inicial)
                                                                                                        ponto_partida_dict = {
                                                                                                                'destino': 'Itupeva, SP',
                                                                                                                'distancia': 0,
                                                                                                                'Número da nota': '',
                                                                                                                'volumes': '',
                                                                                                                'Duração': '',
                                                                                                                'coordenadas': ponto_partida,
                                                                                                                'coordenadas_google': f'{lat_inicial},{lon_inicial}',
                                                                                                                'cliente': ''
                                                                                                            }
                                                                                                        if ponto_partida_dict['coordenadas_google'] in destinos_info:
                                                                                                            pass
                                                                                                        else:
                                                                                                            destinos_info.append(ponto_partida_dict['coordenadas_google'])
                                                                                        destino = nota['Destino']
                                                                                            
                                                                                        address = f"{destino}"
                                                                                        base_url = "https://maps.googleapis.com/maps/api/geocode/json"
                                                                                        params = {
                                                                                                        "address": address,
                                                                                                        "key": st.secrets['firebase']['chave_api_googlemaps']  # Substitua pela sua chave de API
                                                                                                    }
                                                            
                                                                                        response = requests.get(base_url, params=params)
                                                                                        data = response.json()
                                                                                        if data["status"] == "OK":
                                                                                                        location = data["results"][0]["geometry"]["location"]
                                                                                                        lat_final = location["lat"]
                                                                                                        lon_final = location["lng"]
                                                                                                        localizacao = f'{lat_final},{lon_final}'
                                                                                                        if localizacao in destinos_info:
                                                                                                            pass
                                                                                                        else:
                                                                                                            destinos_info.append(localizacao)
                                                                        final_route_url = base_url2 + '/'.join(destinos_info)
                                                                        botao = st.link_button('Acessar rota',final_route_url)
        except:
                                                                      st.error('Sem Roteiros Disponíveis')
elif seletor == "suporte inteligente":
       time.sleep(0.5)
       msg1 = st.toast('Seja Bem vindo (a)') 
       time.sleep(0.5) 
       msg2 = st.toast('Sou seu assistente personalizado. Minha função é trazer respostas acerca de perguntas sobre as notas processadas independentemente do perído')  
       texto_ia = st.text_input(label='',placeholder='Pergunte-me algo')
       if texto_ia:
           try:
              ia(pergunta=texto_ia)
           except:
               st.error('Não foram encotrados Roteiros')

        
              
              

            
      

    

    
