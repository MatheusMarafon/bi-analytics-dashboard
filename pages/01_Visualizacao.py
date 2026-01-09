import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Visualização", layout="wide")
st.header("Visualização e Gráficos")

dados_vendas = {
    "Produto": ["Teclado", "Mouse", "Monitor", "Notebook"],
    "Preço": [150.50, 80.00, 900.00, 4500.00],
}
st.dataframe(pd.DataFrame(dados_vendas), use_container_width=True)

# Gráfico rápido de exemplo
fig = px.bar(
    pd.DataFrame(dados_vendas), x="Produto", y="Preço", title="Preços por Produto"
)
st.plotly_chart(fig, use_container_width=True)
