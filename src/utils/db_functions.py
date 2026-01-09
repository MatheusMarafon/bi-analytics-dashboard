# Nome do arquivo: db_functions.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine


# --- Cache de Conexão (Global) ---
@st.cache_resource
def configurar_conexao():
    """Cria e armazena o engine de conexão com o banco."""
    try:
        db = st.secrets["postgres"]
        conn_url = (
            f"postgresql://{db['user']}@{db['host']}:{db['port']}/{db['database']}"
        )
        return create_engine(conn_url)
    except Exception as e:
        st.error(f"Erro ao configurar conexão global: {e}")
        return None


# --- Cache de Dados ---
@st.cache_data(ttl=600)
def buscar_dados_otimizados(query_string, _engine):
    """Executa a query e armazena o resultado em cache."""
    with _engine.connect() as conn:
        df = pd.read_sql(query_string, conn)
    return df


@st.cache_data
def listar_tabelas(_engine):
    """Lista as tabelas públicas do banco."""
    query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
    with _engine.connect() as conn:
        return pd.read_sql(query, conn)["table_name"].tolist()
