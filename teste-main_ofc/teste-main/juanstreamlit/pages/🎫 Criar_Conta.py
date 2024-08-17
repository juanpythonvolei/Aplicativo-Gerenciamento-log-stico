import streamlit as st
import requests
st.markdown("""
    <style>
       [aria-expanded='true'] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)
key = 'AIzaSyDKr5U-JLK2SvlndWbdNULNCCJNRYVv4rg'
col1,col2,col3 = st.columns(3)
image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
login = st.text_input(label='',placeholder='Digite E-mail de criação de conta')
if login:
    senha = st.text_input(label='',type="password",placeholder='Digite sua senha de criação de conta')
    if senha:
        data = {"email":login,"password":senha,"returnSecureToken":True}
        requisicao = requests.post(f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={key}",data=data)
        requisicao_dic = requisicao.json()
        if requisicao.ok:
                    st.switch_page('pages/🌐 Processamento.py')
        else:
            mensagem_erro  = requisicao_dic['error']['message']
            if mensagem_erro == 'EMAIL_EXISTS':
                mensagem_erro = 'E-mail já foi cadastrado'
                st.error(mensagem_erro)
            else:
                st.error(mensagem_erro)
botao_voltar = st.button('Voltar para a tela do login')
with col2:
    if botao_voltar:
            st.switch_page("Login.py")
