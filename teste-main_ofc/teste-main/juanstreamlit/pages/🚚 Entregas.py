import streamlit as st
import requests
from streamlit_carousel import carousel
import time
from firebase_admin import credentials, firestore,db

image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')

requisicao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requisicao.json()
     
          
dados = roteiro['bancodedadosroteirooficial']
       
seletor1,seletor2 = st.tabs(['Entregas','Comprovantes'])
with seletor1:# Exibe a seleção da data
     if 'fotos' not in st.session_state:
          st.session_state.fotos = []
     lista_total = [item for item in dados if item!= 'Comprovantes']
     lista_nomes = []
     lista_destinos = []
     destinos_info = []
     distancia_total = 0
     lista_verificada = []
     dados2 = roteiro['Veículos']
     for item in dados2:            
                                      veiculo = dados2[f'{item}']
                                      for elemento in veiculo:
                                             espec = veiculo[f'{elemento}']
                                             nome = espec['nome']
                                             lista_nomes.append(nome)
            # Carrega os dados do banco de dados
     checkbox_states = {}
     opcao_selecionada_data = st.selectbox("", lista_total,index=None,placeholder='Selecione uma data')
     if opcao_selecionada_data:
               for item in dados:
                                   if item != 'Comprovantes':
                                                  roteiro = dados[f'{item}']
                                                  for elemento in roteiro:
                                                                   nota = roteiro[f'{elemento}']
                                                                   data_emit = nota['Data de Emissão']
                                                                   if str(data_emit) == str(opcao_selecionada_data):
                                                                          y = nota['Veículo']      
                                                                          for i in y:
                                                                              try:
                                                                                  veiculo = y[f'{i}']['Veículo']
                                                                                  if veiculo in lista_verificada:
                                                                                       pass
                                                                                  else:   
                                                                                       lista_verificada.append(veiculo)           
                                                                              except:
                                                                                lista_verificada.append('Indefinido')
               if 'Indefinido' in lista_verificada:                                                  
                    veiculo = st.selectbox('',lista_nomes,index = None,placeholder='Selecione um Veículo')
               else:
                    veiculo = st.selectbox('',lista_verificada,index = None,placeholder='Selecione um Veículo')
          
               if veiculo:
               
                      try:
                          lista_alerta = []
                          lista_conferida = []
                          lista_notas = []
                          for item in dados:
                                                  
                                                  roteiro = dados[f'{item}']
                                                  for elemento in roteiro:
                                                              nota = roteiro[f'{elemento}']
                                                              data_emit = nota['Data de Emissão']
                                                              if str(data_emit) == str(opcao_selecionada_data):
                                                                status = nota['status']
                                                                if status == 'Entrega não completa':
                                                                     volumes = nota['Volumes']
                                                                     numero_nota = nota['Número da Nota']
                                                                     lista_notas.append(numero_nota)
                                                                     valor = nota['Valor Total']
                                                                     cliente = nota['Cliente']
                                             
                                                                     # Usa colunas para organizar a checkbox e o camera_input lado a lado
                                                                     col1, col2 = st.columns([3, 1])
                                                                     with col1:
                                                                         checkbox_states[numero_nota] = st.checkbox(f"Cliente: {cliente}. Nota: {numero_nota}. Volumes: {volumes}", key=numero_nota)
                                                                     with col2:
                                                                         image = st.camera_input(f"Foto para Nota {numero_nota}", key=f"camera_{numero_nota}")
                                                                         if image:
                                                                              with open(f'captured_image_{numero_nota}.jpg', 'wb') as f:
                                                                                  f.write(image.getvalue())
                                                                              link = f"./captured_image_{numero_nota}.jpg"  
                                                                              if link not in st.session_state.fotos:
                                                                                   st.session_state.fotos.append(link)
                                                                              else:
                                                                                   pass
                                             
                                                                else: 
                                                                     st.success('Entrega Completa')  
                                                                
                                                                        
                                                       
                      except:
                            pass
                        
                        
                            
                            # Agora você pode usar o dicionário 'checkbox_states' conforme necessário
                        
                      for nota, estado in checkbox_states.items():   
                                if estado:
                                    status = 'Feito'
                                    lista_conferida.append(status)
                                    if len(lista_conferida) == len(lista_notas):
                                                requisicao_1 = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
                                                roteiro_1 = requisicao.json()
                                                dados_1 = roteiro_1['bancodedadosroteirooficial']
                                                for item in dados_1:
                                                              roteiro = dados_1[f'{item}']
                                                              for elemento in roteiro:
                                                                  nota = roteiro[f'{elemento}'] 
                                                                  data = nota['Data de Emissão']
                                                                  
                                                                  if data == opcao_selecionada_data:
                                                                    status = nota['status']
                                                                    link = f'https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/bancodedadosroteirooficial/{opcao_selecionada_data}/{elemento}/status.json'
                                                                    dados = '{"status": "Entrega realizada"}'
                                                                    requests.patch(link, data=dados)        
                                                                    link2 = f'https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/bancodedadosroteirooficial/{opcao_selecionada_data}/{elemento}/Veículo.json'
                                                                    dados2 = {"Veículo": veiculo}
                                                                    requests.post(link2, json=dados2)
                                                link3 = f'https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/bancodedadosroteirooficial/Comprovantes.json'
                                                dados3 = {"Comprovantes": st.session_state.fotos}
                                                requests.post(link3, json=dados3)                                                 
                                                st.success('Entrega realizada com Sucesso')
                                                   
                                                
                                               
                                                
                                                                
                                                      
                                    else:
                                                pass
                                else:
                                    try:
                                                status = 'Feito'
                                                lista_conferida.remove(status)
                                    except:
                                                pass
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
                      
                      st.markdown(f"<style>{css_style}</style>", unsafe_allow_html=True)   
                      
                              
                              # Estilização CSS embutida
                      
                     
                                                         
                                                    
                      try:   
                        lista = []
                        for a in dados:
                                                    
                                                    roteiro = dados[f'{a}']
                                                    for elemento in roteiro:
                                                                nota = roteiro[f'{elemento}']
                                                                data_emit = nota['Data de Emissão']
                                                                if str(data_emit) == str(opcao_selecionada_data):
                                                                  numero_nota = nota['Número da Nota']
                                                                  lista.append(numero_nota)
                                                                  status = nota['status']
                      
                                                    
                                                                  
                      except:   
                        pass  
              
                      if  status == 'Entrega não completa':   
                                                           
                                                                                
                                                                                metrica1 = st.metric(label="Total de notas completas", value=len(lista_conferida))            
                      
                                    
                      else:        
                                                                                metrica1 = st.metric(label="Total de notas completas", value=len(lista))  
with seletor2:
      lista_comprovantes = []
      for item in dados:
                                   if item == 'Comprovantes':
                                        secao = dados[f'{item}']
                                        st.write(secao)    
      st.selctbox(label='',placeholder = 'selecione uma nota',options = lista_comprovantes)
