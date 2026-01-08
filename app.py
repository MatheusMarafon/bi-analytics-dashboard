import streamlit as st

# Configurações da página
st.set_page_config(page_title="Estudo Dashboard", layout="centered")

# Título do projeto
st.title("Hello, World!")

st.header("Semana 1: Dia 01(Segunda).")
st.write("Entregável do dia 01 - 'app.py' rodando streamlit com 'st.write'.")

if st.button("Clique para validar o site"):
    st.success("Site validado com sucesso!")
    st.balloons()