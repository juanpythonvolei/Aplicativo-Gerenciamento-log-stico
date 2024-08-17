import streamlit as st
import requests
from streamlit_carousel import carousel
import time

if 'fotos' not in st.session_state:
  st.session_state.fotos = []
image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
try:
     requisicao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
     roteiro = requisicao.json()
     
          
     dados = roteiro['bancodedadosroteirooficial']
       
         # Exibe a seleção da data
     lista_total = [item for item in dados]
     lista_nomes = []
     lista_verificada_sim =[]
     lista_verificada_nao = []
     lista_nomes_ja_entregaram = []
     lista_destinos = []
     destinos_info = []
     distancia_total = 0
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
                                             
                                             roteiro = dados[f'{item}']
                                             for elemento in roteiro:
                                                         nota = roteiro[f'{elemento}']
                                                         data_emit = nota['Data de Emissão']
                                                         if str(data_emit) == str(opcao_selecionada_data):
                                                              if nota['Veículo'] =='Indefinido':
                                                                 lista_verificada_nao.append('Indefinido')
                                                                
                                                              else:
                                                                   for item in nota['Veículo']:
                                                                        carro = nota['Veículo'][f'{item}']
                                                                        lista_nomes_ja_entregaram.append(carro['Veículo'])
                                                                        lista_verificada_sim.append('sim')
          if 'Indefinido' in lista_verificada_nao:                                                              
               veiculo = st.selectbox('',lista_nomes,index = None,placeholder='Selecione um Veículo')
          else:
               veiculo = st.selectbox('',list(set(lista_nomes_ja_entregaram)),index = None,placeholder='Selecione um Veículo')
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
                                                             col1, col2 = st.columns([3, 1])                      
                                                                                   
                                                                                       # Usa o dicionário para controlar o estado da checkbox
                                                             
                                                             with col1:
                                                              checkbox_states[numero_nota] = st.checkbox(f"Cliente: {cliente}. Nota: {numero_nota}. Volumes: {volumes}", key=numero_nota)
                                                             with col2:
                                                                    image = st.camera_input(f"Foto Comprovante Nota {numero_nota}", key=f"camera_{numero_nota}")  
                                                                    if image:
                                                                      with open(f'captured_image_{Veículo}.jpg', 'wb') as f:
                                                                          f.write(image.getvalue())
                                                                      link = f"./captured_image_{Veículo}.jpg" 
                                                                      st.session_state.fotos.append(link)
                                                                    else:
                                                                        pass 
                                                             st.divider()  
                                                            
                                                             
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
                                           if len(st.session_state.fotos) > 0:                      
                                             link3 = f'https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/bancodedadosroteirooficial/{opcao_selecionada_data}/Fotos dos Comprovantes.json'
                                             dados3 = {"Veículo": st.session_state.fotos}   
                                             requests.post(link3, json=dados3)
                                           else:
                                             pass  
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
except:
      st.error('Não há roteiros disponíveis')
