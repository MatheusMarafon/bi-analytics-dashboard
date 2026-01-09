import streamlit as st
import pandas as pd
import plotly.express as px
from database import configurar_conexao, calcular_metricas_negocio

st.set_page_config(page_title="Dashboard Executivo", layout="wide")

st.title("📊 Análise de Performance e Retenção")

# --- STORYTELLING: Contexto Inicial ---
st.markdown(
    """
Esta visão fornece um diagnóstico da saúde financeira e da base de clientes. 
O objetivo é identificar se o crescimento da receita está acompanhado pela fidelização da base.
"""
)

engine = configurar_conexao()

if engine:
    with st.spinner("Analisando dados históricos..."):
        m = calcular_metricas_negocio(engine)

    # --- SEÇÃO 1: Saúde Financeira ---
    st.subheader("1. Eficiência Financeira")
    st.markdown(
        "> **Insight:** O Ticket Médio reflete o valor gerado por cada transação. Se este valor cai, precisamos aumentar o volume de vendas para manter a receita."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Ticket Médio", f"R$ {m['ticket']:,.2f}", delta="1.2%")

    st.markdown("---")

    # --- SEÇÃO 2: Comportamento do Cliente ---
    st.subheader("2. Fidelização e Risco de Evasão")

    c_left, c_right = st.columns([1, 2])

    with c_left:
        st.markdown(
            f"""
        **Análise de Churn:**
        Atualmente, nossa taxa de cancelamento está em **{m['churn']:.1f}%**. 
        
        * **Ação Recomendada:** Se o Churn ultrapassar 5%, é necessário revisar as estratégias de Customer Success.
        * **Retenção:** Mantemos **{m['retencao']:.1f}%** da base ativa, o que indica uma boa aderência ao produto.
        """
        )
        st.metric("Churn Rate", f"{m['churn']:.1f}%", delta="-0.5%")

    with c_right:
        df_pizza = pd.DataFrame(
            {"Status": ["Retidos", "Churn"], "Percentual": [m["retencao"], m["churn"]]}
        )
        fig = px.pie(
            df_pizza,
            values="Percentual",
            names="Status",
            color_discrete_sequence=["#2ecc71", "#e74c3c"],
            hole=0.4,
        )
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, width="stretch")

    st.markdown("---")

    # --- SEÇÃO 3: Conclusões e Próximos Passos ---
    st.subheader("3. Conclusão Estratégica")
    if m["churn"] < 2:
        st.success("Operação Saudável: Foco total em aquisição de novos clientes.")
    else:
        st.warning(
            "Alerta de Retenção: Focar em entender o motivo da saída dos clientes atuais."
        )

else:
    st.error("Conexão com o banco indisponível para análise.")
