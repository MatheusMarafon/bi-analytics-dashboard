import streamlit as st
import pandas as pd
import numpy as np
from database import configurar_conexao, buscar_dados_otimizados

st.set_page_config(page_title="Dashboards", layout="wide")

st.title("Painel de Indicadores de Performance")

# --- TAREFA: Calcular métricas comparativas ---

# Simulando dados de vendas de dois meses para cálculo de delta
vendas_mes_atual = 15200.50
vendas_mes_anterior = 13800.00
variacao_vendas = ((vendas_mes_atual - vendas_mes_anterior) / vendas_mes_anterior) * 100

vagas_abertas_hoje = 45
vagas_abertas_ontem = 48
variacao_vagas = vagas_abertas_hoje - vagas_abertas_ontem

# --- TAREFA: Implementar st.metric com delta ---

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Receita Mensal",
        value=f"R$ {vendas_mes_atual:,.2f}",
        delta=f"{variacao_vendas:.1f}% vs mês anterior",
    )

with col2:
    st.metric(
        label="Vagas Ativas",
        value=vagas_abertas_hoje,
        delta=variacao_vagas,
        delta_color="inverse",  # Vermelho se aumentar, verde se diminuir (útil para custos ou problemas)
    )

with col3:
    # Exemplo de métrica neutra (apenas o valor atual)
    st.metric(label="Consultas SQL", value=st.session_state.contador_consultas)

with col4:
    st.metric(label="Conversão de Candidatos", value="12.5%", delta="+2.1%")

st.markdown("---")

# Visualização de suporte (Tabela de tendência)
st.subheader("Histórico de Performance")
df_tendencia = pd.DataFrame(
    {
        "Mês": ["Jan", "Fev", "Mar", "Abr"],
        "Receita": [12000, 13800, 15200, 14900],
        "Meta": [11000, 13000, 15000, 15000],
    }
)
st.line_chart(df_tendencia.set_index("Mês"), width="stretch")
