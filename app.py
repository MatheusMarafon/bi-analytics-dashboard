import streamlit as st

st.set_page_config(page_title="Home - Dashboard BI", layout="wide")

# Inicialização Global do Session State (fica aqui pois é a primeira página a rodar)
if "contador_consultas" not in st.session_state:
    st.session_state.contador_consultas = 0

if "historico_tabelas" not in st.session_state:
    st.session_state.historico_tabelas = []

st.title("Sistema de Inteligência de Dados")
st.markdown("---")

st.markdown(
    """
### Bem-vindo à nova estrutura multipágina!
Navegue pelo menu à esquerda para acessar os módulos:
1. **Visualização:** Dados rápidos e tabelas.
2. **Explorador SQL:** Consultas dinâmicas e inserção de dados.
"""
)

st.sidebar.success("Selecione uma página acima.")
