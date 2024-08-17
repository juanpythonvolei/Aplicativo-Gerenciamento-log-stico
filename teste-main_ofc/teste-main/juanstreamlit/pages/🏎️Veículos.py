import streamlit as st
import requests
import pandas as pd
from streamlit_option_menu import option_menu
import math
from geopy.distance import geodesic
from firebase_admin import credentials, firestore,db
from streamlit_calendar import calendar
import datetime
from streamlit_carousel import carousel
import time
image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
seletor1,seletor2,seletor3 = st.tabs(['Cadastrar Veículos','Pesquisar Veículos','Excluir veículos'])
time.sleep(0.5)
msg1 = st.toast('Bem vindo (a) a área de cadastro')
time.sleep(0.5)
msg2 = st.toast('Nessa aba, você pode cadastrar veículos para a frota, ou, vizualizar informações dos cadastrados')
@st.dialog(f"Deseja realmente cadastrar o veículo? ")             
def escolha(Veículo,dict_veiculo):    
                                                            
                                                            sim = st.button('Sim')
                                                            if sim:
                                                              try:
                                                                ref.child(Veículo).push().set(dict_veiculo)
                                                                st.success(f'Veículo: {Veículo} cadastrado com sucesso')
                                                              except:
                                                                st.error('Não há saida de dados disponível')
                                                            else:
                                                                st.info(f'Você ainda não cadastrou o veículo {Veículo}')
@st.dialog(f"Deseja realmente acessar a rota da nota?") 
def escolha2(excluir):    
                                                            
                                                            sim = st.button('Sim')
                                                            if sim:
                                                                    veiculo_ref = db.reference(f'Veículos/{excluir}')
                                                                    veiculo_ref.delete()
                                                                    st.success(f'Veículo {excluir} excluido')
                                                            else:
                                                              st.info(f'Você realmente deseja excluir o veículo {excluir}')
#seletor  = option_menu("Menu Principal", ["Cadastrar Veículos", "Pesquisar Veículos"], icons=["truck", "search"],menu_icon=['menu-button-wide-fill'])
ref = db.reference('Veículos')
with seletor1 :
    Veículo = st.text_input(label='',placeholder='Digite o nome do Veículo')
    if not Veículo:
      st.warning('Você ainda não forneceu o nome do veículo')
    Placa = st.text_input(label='',placeholder='Digite a placa do veículo')
    if not Placa:
      st.warning('Você ainda não forneceu a placa do veículo')
    km = st.number_input("",placeholder='Selecione a relação km/L do veículo',value=None)
    if not km:
      st.warning('Você ainda não forneceu o km/l do veículo')
    distancia_inicial = st.number_input("",placeholder='Selecione a kilometragem atual do veículo',value=None)
    if not distancia_inicial:
      st.warning('Você ainda não forneceu a kilometragem inicial do veículo')
    foto = st.text_input(label='',placeholder='Insira a url da foto do Veículo')  
    if not foto:
      st.warning('Você ainda não forneceu a foto do veículo')
    if Veículo and Placa and km and foto:
              dict_veiculo = {'nome':Veículo,
                              'Placa':Placa,
                              'Km':km,
                             'Foto':foto,
                             'Distância':'Nenhuma',
                             'Kilometragem':distancia_inicial}
              botao = st.button('Cadastrar Veículo')
              if botao:
                      escolha(Veículo,dict_veiculo)
with seletor2 :
  try:
            requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
            roteiro = requiscao.json()
            dados = roteiro['Veículos']
            lista_nomes = []
            for item in dados:
                                veiculo = dados[f'{item}']
                                for elemento in veiculo:
                                       espec = veiculo[f'{elemento}']
                                       nome = espec['nome']
                                       lista_nomes.append(nome)
            opcao = st.selectbox('',lista_nomes,index=None,placeholder='Selecione um veículo')
            if opcao:
                    for item in dados:
                                        veiculo = dados[f'{item}']
                                        for elemento in veiculo: 
                                               espec = veiculo[f'{elemento}']
                                               nome = espec['nome'] 
                                               if nome == opcao: 
                                                 km = espec['Kilometragem'] 
                    distancia_total = float(km)
                    km = km
                    lista_notas = []
                    lista_veiculos = []
                    lista_locais = []
                    destinos_info = []
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
                                                            origem_atual = (lat_inicial, lon_inicial)
                    requiscao2 = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
                    roteiro2 = requiscao2.json()        
                    dados2 = roteiro2['bancodedadosroteirooficial']    
                    for item in dados2:
                                          
                                          roteiro = dados2[f'{item}']
                                          for elemento in roteiro:
                                                      nota = roteiro[f'{elemento}']
                                                      lista_notas.append(nota)
                                                      y = nota['Veículo']  
                                                      for i in y:
                                                          try:
                                                              veiculo = y[f'{i}']['Veículo']
                                                          except:
                                                              pass
                                                          if str(veiculo) == str(opcao):
                                                              if len(lista_veiculos) <= len(lista_notas):
                                                                  lista_veiculos.append(veiculo)
                                                                  destino = nota['Destino']
                                                                  mass = nota['Massa']
                                                                  lista_locais.append(destino)
                                                              else:
                                                                  pass
                    for item in list(set(lista_locais)):
                                                          
                        address = f"{item}"
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
                    for i in range(len(destinos_info)):
                          destino_info = destinos_info[i]
                          lat_final, lon_final = map(float, destino_info.split(','))  # Obtém as coordenadas do destino
                          
                          # Constrói a URL da matriz de distância
                          distance_matrix_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origem_atual[0]},{origem_atual[1]}&destinations={lat_final},{lon_final}&key={st.secrets['firebase']['chave_api_googlemaps']}"
                          
                          # Faz a requisição
                          response = requests.get(distance_matrix_url)
                          data = response.json()
                          
                          if data["status"] == "OK":
                              try:
                                  distance_text = data["rows"][0]["elements"][0]["distance"]["text"]
                                  distance_value = float(distance_text.split()[0]) 
                                  distancia_total += distance_value 
                                  duration = data["rows"][0]["elements"][0]["duration"]["text"]
                              except:
                                  pass
                              # Agora você pode usar 'distance' e 'duration' conforme necessário
                      
                              # Atualiza a origem para o próximo destino
                          origem_atual = (lat_final, lon_final)
                    for item in dados:
                                        veiculo = dados[f'{item}']
                                        for elemento in veiculo: 
                                               espec = veiculo[f'{elemento}']
                                               nome = espec['nome']
                                               if nome == opcao: 
                                                   link = espec['Foto']
                                                   st.image(link) 
                                                   placa = espec['Placa']
                                                   kilometragem = espec['Km']
                                                   total_gasto = f'{(5.50*distancia_total)/kilometragem:.2f} R$'
                                                   dict = {'Nome':nome,'Placa':placa,'Km/l':kilometragem,'Total de Viagens realizadas':len(list(set(lista_locais))),'Distancia Total Percorrida':f'{distancia_total:.2f} Km','Kilometragem Inicial':f'{km:.2f} km','Total de Combustível Gasto':total_gasto}
                                                   st.table(dict)
            else:
              st.info('Selecione um Veículo para que seja possível realizar a pesquisa')
  except:
    st.error('Não há saida de dados disponível')
with seletor3:
   try:
        requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
        roteiro = requiscao.json()
        dados = roteiro['Veículos']
        lista_nomes = []
        for item in dados:
                            veiculo = dados[f'{item}']
                            for elemento in veiculo:
                                   espec = veiculo[f'{elemento}']
                                   nome = espec['nome']
                                   lista_nomes.append(nome)
        excluir = st.selectbox(label='',options = lista_nomes,index=None,placeholder='Selecione um veículo para excluir')
        if excluir:
            try:
    
                                                                    escolha2(excluir)
            except:  
                    st.error(f'Não foi possível excluir o veículo {excluir}')
   except: 
      st.error('Não há banco de dados')
