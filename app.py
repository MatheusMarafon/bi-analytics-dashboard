import streamlit as st
import pandas as pd

# Configurações da página
st.set_page_config(page_title="Estudo Dashboard", layout="wide")

# Dia 01: Hello World
st.title("Hello, World!")
st.write("Bem-vindo ao meu dashboard de BI com Streamlit")
st.markdown("---")

# Dia 02: Input Widgets
st.sidebar.header("Filtros do Dashboard")

# Selectbox (Seleção Única)
st.sidebar.subheader("Localização")
cidade = st.sidebar.selectbox(
    "Escolha a cidade:",
    options=["São Paulo", "Rio de Janeiro", "Curitiba", "Belo Horizonte"],
)

# Multiselect (Seleção Múltipla)
st.sidebar.subheader("Categorias")
tecnologias = st.sidebar.multiselect(
    "Selecione as tecnologias:",
    options=["Python", "SQL", "Airflow", "Docker", "AWS"],
    default=["Python", "SQL"],
)

# Slider (Intervalo)
st.sidebar.subheader("Experiência")
anos_xp = st.sidebar.slider("Anos de experiência na área:", 0, 20, 1)

# Dia 03: Display de Dados
st.header("Dia 03: Displau de Dados")

# Criando um DataFrame de exemplo (simulando carga de csv)
dados_vendas = {
    'Produto': ['Teclado', 'Mouse', 'Monitor', 'Notebook'],
    'Preço': [150.50, 80.00, 900.00, 4500.00],
    'Estoque': [15, 30, 10, 5]
}
df = pd.DataFrame(dados_vendas)

col_esq, col_dir = st.columns(2)

with col_esq:
    st.subheader("Visualização Interativa (st.dataframe)")
    st.dataframe(df, use_container_width=True)

with col_dir:
    st.subheader("Visualização Estática (st.table)")
    st.table(df)

# Exibindo resultados
st.markdown("---")
st.header("Visualização de Filtros (Dia 02)")
col1, col2 = st.columns(2)

with col1:
    st.info(f"**Cidade selecionada:** {cidade}")
    st.info(f"**Anos de experiência:** {anos_xp}")

with col2:
    st.success(f"**Tecnologias focadas:** {', '.join(tecnologias)}")

# Exemplo de lógica
if anos_xp > 5:
    st.write("Perfil com experiência avançada detectado!")
else:
    st.write("Perfil em desenvolvimento de carreira.")