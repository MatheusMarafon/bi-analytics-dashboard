import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("Indicadores e Gráficos")

# Sidebar (Os filtros que você tinha antes)
st.sidebar.header("Filtros")
cidade = st.sidebar.selectbox("Cidade:", ["São Paulo", "Rio de Janeiro", "Curitiba"])
anos_xp = st.sidebar.slider("Anos de XP:", 0, 20, 5)

# Conteúdo das antigas abas de gráficos
st.subheader(f"Análise para {cidade}")
df_demo = pd.DataFrame({"Tech": ["Python", "SQL"], "Demanda": [80, 60]})
fig = px.bar(df_demo, x="Tech", y="Demanda", color="Tech")
st.plotly_chart(fig, use_container_width=True)
