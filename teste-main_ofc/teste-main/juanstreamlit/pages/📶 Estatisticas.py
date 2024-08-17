import streamlit as st
import requests
import pandas as pd
from streamlit_option_menu import option_menu
import math
from geopy.distance import geodesic
import time


image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
lista_total = []
destinos_info = []
requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requiscao.json()

dados = roteiro['bancodedadosroteirooficial']
base_url2 = "https://www.google.com/maps/dir/"   

for item in dados:
                  roteiro = dados[f'{item}']
                  lista_total.append(item)
opcao_selecionada = st.selectbox("", lista_total,index=None,placeholder='Selecione uma data')
selected1,selected2 = st.tabs(['Dados Gerais','Dados do Transporte'])
if opcao_selecionada:
        time.sleep(0.5)
        msg1 = st.toast('Bem vindo (a)')
        time.sleep(0.5)
        msg2 = st.toast('Nessa aba, você pode vizualiar os dados gerais das entregas realizadas ou dos tranportes, em função da data selecionada')                
        #selected = option_menu("Menu Principal", ["Dados Gerais", "Dados do Tranporte"], icons=["database", "truck"], default_index=1)
        # Adicionando botões em cada coluna
        with selected1:
                
                texto_nota = []
                lista_produtos = []
                lista_clientes = []
                lista_valores = []
                lista_notas = []
                lista_volumes = []
                valor_total = 0
                
                for item in dados:
                        roteiro = dados[f'{item}']
                        for elemento in roteiro:
                            nota = roteiro[f'{elemento}']
                            if nota['Data de Emissão'] == opcao_selecionada:
                                for item in nota:
                                    numero_nota = nota['Número da Nota']
                                    destino = nota['Destino']
                                    volumes = nota['Volumes']
                                    cliente = nota['Cliente']
                                    Produtos = nota['Produtos'][0]
                                    if nota['status']:
                                      status = nota['status']
                                      if status == 'Entrega não completa':
                                        status = 'Incompleta'
                                      else:
                                        status = 'Completa'
                                    valor  = nota['Valor Total']
                                valor_total += float(valor)
                                texto_nota.append(destino)
                                lista_produtos.append(Produtos)
                                lista_clientes.append(cliente)
                                lista_valores.append(valor)
                                lista_notas.append(numero_nota)
                                lista_volumes.append(volumes)
                
                a = {'Destino': texto_nota,
                          'Valor da nota': lista_valores,
                          'Volumes':lista_volumes,
                          'Cliente':lista_clientes,
                          'Nota':lista_notas}
                df = pd.DataFrame(a)
          
                # Exibindo a tabela no Streamlit
                st.table(df)
                col1, col2, col3 = st.columns(3)
                  
                  # Estilização CSS embutida
                css_style = """
                      .my-square {
                          background-color:#0275b1;
                          border-radius: 10px;
                          display: flex;
                          justify-content: center;
                          align-items: center;
                          color: white;
                      }
                  """
                  
                  # Aplicando o estilo e inserindo os quadrados
                
                
                
                with col1:
                      metrica1 = st.metric("Status", value=str(status))
                with col2:
                      metrica2 = st.metric("Total Destinos", value=f'{len(list(set(texto_nota))):.2f}')
                with col3:
                      metrica3 = st.metric("Valor Total", value=f'{valor_total:.2f}')
          
        with selected2:
              Massa_total = 0
              valor_total = 0
              distancia_total = 0
              lista_duracao = []
              lista_viagem = []
              valor = []
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
              lista_total = []
              destinos_info = []
              requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
              roteiro = requiscao.json()
              dados = roteiro['bancodedadosroteirooficial']
              base_url2 = "https://www.google.com/maps/dir/"
              for item in dados:
                              roteiro = dados[f'{item}']
                              for elemento in roteiro:
                                  nota = roteiro[f'{elemento}']
                                  if nota['Data de Emissão'] == opcao_selecionada:
                                      destino = nota['Destino']
                                      valor  = nota['Valor Total']
                                      valor_total += float(valor)
                                      massa = nota['Massa']
                                      try:
                                        Massa_total += float(massa)
                                      except:
                                        Massa_total = massa
                                      if destino in lista_total:
                                          pass
                                      else:
                                          lista_total.append(destino)
                                          
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
                                                                    
                                                                  
          
                                                                         
              try:
                for i in range(len(destinos_info)):
                        destino_info = destinos_info[i]
                        lat_final, lon_final = map(float, destino_info.split(','))  # Obtém as coordenadas do destino
                        
                        # Constrói a URL da matriz de distância
                        distance_matrix_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origem_atual[0]},{origem_atual[1]}&destinations={lat_final},{lon_final}&key={st.secrets['firebase']['chave_api_googlemaps']}"
                        
                        # Faz a requisição
                        response = requests.get(distance_matrix_url)
                        data = response.json()
                        
                        if data["status"] == "OK":
                            distance_text = data["rows"][0]["elements"][0]["distance"]["text"]
                            distance_value = float(distance_text.split()[0]) 
                            lista_viagem.append(distance_text)
                            distancia_total += distance_value 
                            duration = data["rows"][0]["elements"][0]["duration"]["text"]
                            lista_duracao.append(duration)
                            
                            # Agora você pode usar 'distance' e 'duration' conforme necessário
                    
                            # Atualiza a origem para o próximo destino
                        origem_atual = (lat_final, lon_final)
                
                            
                data = {'Destino': lista_total,
                            'Distância':lista_viagem,
                            'Duração':lista_duracao}
                df = pd.DataFrame(data)
                
                    # Exibindo a tabela no Streamlit
                st.table(df)
            
            
            
            
                # Estilização CSS embutida
                col1, col2, col3 = st.columns(3)
                
                # Estilização CSS embutida
                css_style = """
                    .my-square {
                        background-color:#0275b1;
                        border-radius: 10px;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        color: white;
                    }
                """
                                      
                with col1:
                                          metrica1 = st.metric(label="Total Combustivel Gasto", value=f'{((distancia_total)/10)*5.50:.2f} R$')
                with col2:
                                          metrica2 = st.metric(label="Massa Total", value=f'{Massa_total:.2f} Kg')
                with col3:
                                          metrica3 = st.metric(label="Km Total", value=f'{distancia_total:.2f} Km')
              except:
                st.info('Problemas')
