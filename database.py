import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text


@st.cache_resource
def configurar_conexao():
    try:
        db = st.secrets["postgres"]
        conn_url = (
            f"postgresql://{db['user']}@{db['host']}:{db['port']}/{db['database']}"
        )
        return create_engine(conn_url)
    except Exception as e:
        st.error(f"Erro ao configurar conexão global: {e}")
        return None


@st.cache_data(ttl=600)
def buscar_dados_otimizados(query_string, _engine):
    with _engine.connect() as conn:
        df = pd.read_sql(query_string, conn)
    return df


@st.cache_data
def listar_tabelas(_engine):
    query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
    with _engine.connect() as conn:
        return pd.read_sql(query, conn)["table_name"].tolist()


@st.cache_data(ttl=3600)
def calcular_metricas_negocio(_engine):
    """Calcula Ticket Médio, Churn e Retenção para a página de Dashboards."""
    with _engine.connect() as conn:
        try:
            ticket = conn.execute(text("SELECT AVG(valor) FROM vendas")).scalar() or 0
            total = conn.execute(text("SELECT COUNT(*) FROM clientes")).scalar() or 1
            inativos = (
                conn.execute(
                    text("SELECT COUNT(*) FROM clientes WHERE status = 'inativo'")
                ).scalar()
                or 0
            )
            churn = (inativos / total) * 100
            return {
                "ticket": float(ticket),
                "churn": float(churn),
                "retencao": 100 - churn,
            }
        except:
            return {"ticket": 0.0, "churn": 0.0, "retencao": 100.0}
