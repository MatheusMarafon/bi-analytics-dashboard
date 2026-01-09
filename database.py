import streamlit as st
import pandas as pd
from sqlalchemy import create_engine


@st.cache_resource
def configurar_conexao():
    try:
        db = st.secrets["postgres"]
        conn_url = (
            f"postgresql://{db['user']}@{db['host']}:{db['port']}/{db['database']}"
        )
        return create_engine(conn_url)
    except Exception as e:
        st.error(f"Erro na conexão: {e}")
        return None


@st.cache_data(ttl=600)
def buscar_dados_otimizados(query_string, _engine):
    with _engine.connect() as conn:
        return pd.read_sql(query_string, conn)


@st.cache_data
def listar_tabelas(_engine):
    query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
    with _engine.connect() as conn:
        return pd.read_sql(query, conn)["table_name"].tolist()
