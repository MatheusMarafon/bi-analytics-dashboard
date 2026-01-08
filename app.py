import streamlit as st
import pandas as pd

# Configurações da página
st.set_page_config(page_title="Estudo Dashboard", layout="wide")

# --- Dia 02: Sidebar (Layout Avançado) ---
st.sidebar.header("Filtros do Dashboard")

st.sidebar.subheader("Localização")
cidade = st.sidebar.selectbox(
    "Escolha a cidade:",
    options=["São Paulo", "Rio de Janeiro", "Curitiba", "Belo Horizonte"],
)

st.sidebar.subheader("Categorias")
tecnologias = st.sidebar.multiselect(
    "Selecione as tecnologias",
    options=[
        "Python",
        "SQL",
        "HTML",
        "CSS",
        "React",
        "React Native",
        "JavaScript",
        "Java",
        "C",
        "C#",
    ],
    default=["Python", "SQL"],
)

st.sidebar.subheader("Experiência")
anos_xp = st.sidebar.slider("Anos de experiência na área:", 0, 20, 1)

# --- Dia 04: Layout Avançado (Tabs e Colunas)
st.title("Estrutura de Layout Avançada")

tab_home, tab_dados, tab_filtros = st.tabs(
    ["Início", "Visualização de Dados", "Análise de Filtros"]
)

with tab_home:
    st.header("Hello, World!")
    st.write("Bem-vindo ao meu Dashboard de BI com Streamlit")
    st.info("Navegue pelas abas acima para ver a evolução do projeto.")

with tab_dados:
    st.header("Dia 03: Display de Dados")

    dados_vendas = {
        "Produto": ["Teclado", "Mouse", "Monitor", "Notebook"],
        "Preço": [150.50, 80.00, 900.00, 4500.00],
        "Estoque": [15, 30, 10, 5],
    }
    df = pd.DataFrame(dados_vendas)

    col_esq, col_dir = st.columns(2)
    with col_esq:
        st.subheader("Interativo (st.dataframe)")
        st.dataframe(df, width="stretch")
    with col_dir:
        st.subheader("Estático (st.table)")
        st.table(df)

with tab_filtros:
    st.header("Análise de Filtros")

    m1, m2, m3 = st.columns(3)
    m1.metric("Cidade", cidade)
    m2.metric("XP", f"{anos_xp} anos")
    m3.metric("Tecnologias", len(tecnologias))

    st.markdown("---")

    col_info1, col_info2 = st.columns([1, 1])
    with col_info1:
        st.success(f"**Tecnologias focadas:** {', '.join(tecnologias)}")

    with col_info2:
        if anos_xp > 5:
            st.write("Perfil com experiência avançada detectado!")
        else:
            st.write("Perfil em desenvolvimento de carreira.")
