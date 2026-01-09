import streamlit as st
import pandas as pd
import time
from sqlalchemy import text
from database import configurar_conexao, buscar_dados_otimizados, listar_tabelas

st.set_page_config(page_title="Explorador SQL", layout="wide")
st.header("🗄️ Explorador de Banco de Dados")

engine = configurar_conexao()

if engine:
    # Feedback visual (Sexta-feira)
    st.info(
        f"🔢 Consultas realizadas nesta sessão: {st.session_state.contador_consultas}"
    )

    lista = listar_tabelas(engine)
    if lista:
        tabela = st.selectbox("Selecione a tabela:", lista)

        # Histórico (Session State)
        if tabela not in st.session_state.historico_tabelas:
            st.session_state.historico_tabelas.append(tabela)

        with engine.connect() as conn:
            colunas = pd.read_sql(
                f"SELECT * FROM {tabela} LIMIT 0", conn
            ).columns.tolist()

        cols_sel = st.multiselect("Colunas:", colunas, default=colunas[:3])

        if st.button("Executar Consulta"):
            with st.spinner("Buscando dados..."):
                st.session_state.contador_consultas += 1
                query = f"SELECT {', '.join(cols_sel)} FROM {tabela} LIMIT 100"
                df = buscar_dados_otimizados(query, engine)
                st.toast("Consulta finalizada com sucesso")
                st.dataframe(df, width="stretch")

        # Seu Formulário de INSERT Dinâmico original
        st.markdown("---")
        with st.form("form_registro", clear_on_submit=True):
            st.subheader(f"Inserir em {tabela}")
            novos_dados = {}
            campos = colunas[:4]
            cols_layout = st.columns(len(campos))
            for i, col_name in enumerate(campos):
                with cols_layout[i]:
                    novos_dados[col_name] = st.text_input(f"{col_name}")

            if st.form_submit_button("Salvar no Banco"):
                with st.status("Processando...") as status:
                    try:
                        col_names = ", ".join(novos_dados.keys())
                        placeholders = ", ".join([f":{c}" for c in novos_dados.keys()])
                        query_ins = text(
                            f"INSERT INTO {tabela} ({col_names}) VALUES ({placeholders})"
                        )
                        with engine.begin() as conn:
                            conn.execute(query_ins, novos_dados)
                        status.update(label="Salvo!", state="complete")
                        st.toast("Registro armazenado")
                        st.cache_data.clear()
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        status.update(label="Erro!", state="error")
                        st.error(e)
