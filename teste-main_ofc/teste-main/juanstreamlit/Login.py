import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore,db
import requests
import os

st.session_state.user = ''

if 'user' not in st.session_state:
  st.session_state.user = 'Usuário: nenhum'                                                                
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #FFA421;
        color: white; /* Cor do texto na barra lateral */
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    body {
        background-color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("""
    <style>
       [aria-expanded='true'] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)
image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')

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
if not firebase_admin._apps:
    autenticacao  = {
            "type": st.secrets["firebase"]["type"],
            "project_id": st.secrets["firebase"]["project_id"],
            "private_key_id": st.secrets["firebase"]["private_key_id"],
            "private_key": st.secrets["firebase"]["private_key"],
            "client_email": st.secrets["firebase"]["client_email"],
            "client_id": st.secrets["firebase"]["client_id"],
            "auth_uri": st.secrets["firebase"]["auth_uri"],
            "token_uri": st.secrets["firebase"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
    }

    cred = credentials.Certificate(autenticacao)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://bancodedadosroteirooficial-default-rtdb.firebaseio.com'  # Substitua pelo URL do seu Realtime Database
    })
else:
    pass

# Crie uma instância do cliente Realtime Database
# Define o estilo CSS para centralizar a imagem


# Configuração para ocultar a sidebar


key = st.secrets['firebase']['key_login']
# Exibe a imagem centralizada


col1,col2,col3 = st.columns(3)
login = st.text_input(label='',placeholder='Digite aqui seu E-mail')

if login:
        senha = st.text_input(label='',type="password",placeholder='Digite aqui sua senha')
        st.session_state.user = login
        if senha:
                    data = {"email":login,"password":senha,"returnSecureToken":True}
                    requisicao = requests.post(f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={key}",data=data)
                    requisicao_dic = requisicao.json()
                    if requisicao.ok:
                        st.switch_page('pages/🌐 Processamento.py')
          
                        st.set_page_config(initial_sidebar_state="collapsed",page_title=f"Roterização e suporte. Usuáro logado:{usuario}")
                        st.session_state.user = usuario
                    else:
                        mensagem_erro  = requisicao_dic['error']['message']
                        if mensagem_erro == 'INVALID_LOGIN_CREDENTIALS':
                            mensagem_erro = 'Credenciais de login invalidas'
                            st.error(mensagem_erro)
                        elif mensagem_erro == 'INVALID_EMAIL':
                            mensagem_erro = 'login negado. Insira um e-mail'
                            st.error(mensagem_erro)
        else:
               st.info('Preencha o campo de senha para concluir o login')
    
else:
    st.info('Insira sua e-mail para liberar a senha')
criar_conta = st.button('Não tem uma conta? Crie sua Conta aqui')
with col2:
        if criar_conta:
                st.switch_page('pages/🎫 Criar_Conta.py')
