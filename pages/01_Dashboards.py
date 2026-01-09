import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from database import configurar_conexao, calcular_metricas_negocio

st.set_page_config(page_title="Dashboards", layout="wide")

# Sidebar (Seus filtros originais)
st.sidebar.header("Filtros do Dashboard")
cidade = st.sidebar.selectbox(
    "Escolha a cidade:", ["São Paulo", "Rio de Janeiro", "Curitiba", "Belo Horizonte"]
)
tecnologias = st.sidebar.multiselect(
    "Tecnologias:", ["Python", "SQL", "HTML", "CSS", "React"], default=["Python", "SQL"]
)
anos_xp = st.sidebar.slider("Anos de experiência:", 0, 20, 1)

st.title("📊 Painel de Indicadores")

engine = configurar_conexao()
if engine:
    # Métricas Reais (Semana 5)
    with st.spinner("Calculando métricas..."):
        m = calcular_metricas_negocio(engine)

    col1, col2, col3 = st.columns(3)
    col1.metric("Ticket Médio", f"R$ {m['ticket']:,.2f}", delta="1.2%")
    col2.metric("Churn Rate", f"{m['churn']:.1f}%", delta="-0.5%", delta_color="normal")
    col3.metric("Taxa de Retenção", f"{m['retencao']:.1f}%", delta="+2.0%")

    st.markdown("---")

    # Gráfico Plotly (Seu código original adaptado para 2026)
    st.subheader(f"Demanda em {cidade}")
    df_plotly = pd.DataFrame(
        {
            "Tecnologia": tecnologias if tecnologias else ["Nenhuma"],
            "Demanda": (
                np.random.randint(10, 100, size=len(tecnologias))
                if tecnologias
                else [0]
            ),
        }
    )
    fig = px.bar(
        df_plotly,
        x="Tecnologia",
        y="Demanda",
        color="Tecnologia",
        template="plotly_dark",
    )
    st.plotly_chart(fig, width="stretch")
