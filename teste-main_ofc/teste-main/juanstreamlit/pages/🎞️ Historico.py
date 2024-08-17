import streamlit as st
import requests
from streamlit_option_menu import option_menu
image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
lista_total = []
destinos_info = []
requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requiscao.json()
try:
          dados = roteiro['bancodedadosroteirooficial']
          base_url2 = "https://www.google.com/maps/dir/"
          selected = option_menu("Menu Principal", ["Historico de Entregas", "Produtos das entregas"], icons=["hourglass-split", "shop"], menu_icon=['menu-button-wide-fill'])
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
          if selected == 'Historico de Entregas':
                    for item in dados:
                                try:               
                                          texto_historico = ''
                                          roteiro = dados[f'{item}']
                                          for elemento in roteiro:
                                                  nota = roteiro[f'{elemento}']
                                                  volumes = nota['Volumes']
                                                  data = nota['Data de Emissão']    
                                                  numero_nota = nota['Número da Nota']
                                                  valor = nota['Valor Total']
                                                  cliente = nota['Cliente']
                                                  if nota['status']  == 'Entrega não completa':
                                                          status = 'Incompleta'
                                                  else:
                                                          status = 'Completa'
                                                  historico = f'''\n
                                                  
          Data: {data}\n
          Volumes: {volumes}\n                
          Numero: {numero_nota}\n
          Valor: {valor}\n    
          Cliente: {cliente}\n
          Status: {status}
                                                  
                                                  \n
                                                  '''               
                                                  texto_historico += historico
                                          st.markdown(f'<div class="my-square">{texto_historico}</div>', unsafe_allow_html=True)      
                                except:        
                                        st.error('Roteiro não está disponível')
          elif selected ==  "Produtos das entregas":
                    st.divider()
                    lista_total = []
                    destinos_info = []
                    
                    requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
                    roteiro = requiscao.json()
                    dados = roteiro['bancodedadosroteirooficial']
                    base_url2 = "https://www.google.com/maps/dir/"
                    try:
                              for item in dados:
                                              roteiro = dados[f'{item}']
                                              lista_total.append(item)
                              opcao_selecionada = st.selectbox("", lista_total,index=None,placeholder='Selecione uma data')
                              if opcao_selecionada:
                                        for item in dados:
                                                    Produtos = ''        
                                                    texto_historico = ''
                                                    roteiro = dados[f'{item}']
                                                    for elemento in roteiro:
                                                            nota = roteiro[f'{elemento}']
                                                            data = nota['Data de Emissão']    
                                                            if data == opcao_selecionada:
                                                                      volumes = nota['Volumes']
                                                                      numero_nota = nota['Número da Nota']
                                                                      valor = nota['Valor Total']
                                                                      cliente = nota['Cliente']
                                                                      produtos = nota['Produtos']
                                                                      Produtos += str(produtos)
                                                                      historico = f'''
                                                                      
                              Data: {data}\n              
                              Numero: {numero_nota}\n
                              Produtos: {Produtos}\n
                                                                      
                                                                      
                                                                      '''               
                                                                      texto_historico += historico
                                                    st.markdown(f'<div class="my-square">{texto_historico}</div>', unsafe_allow_html=True)    
                    except:
                                        st.error('Roteiro não está disponível')
except:
                     st.error('Sem Roteiros Disponíveis')
          
    
     


