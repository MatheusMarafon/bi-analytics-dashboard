import streamlit as st

st.set_page_config(page_title="Home", layout="wide")

# INICIALIZAÇÃO: O bloco de notas do usuário começa aqui
if "contador_consultas" not in st.session_state:
    st.session_state.contador_consultas = 0
if "historico_tabelas" not in st.session_state:
    st.session_state.historico_tabelas = []

st.title("Meu Dashboard Multipágina")
st.markdown("---")
st.write("Use o menu ao lado para navegar entre as abas do projeto.")
st.info("O contador de consultas e o histórico são mantidos entre as páginas!")
