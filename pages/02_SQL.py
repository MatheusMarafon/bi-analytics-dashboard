import streamlit as st
import pandas as pd
import time
from sqlalchemy import text
from database import configurar_conexao, buscar_dados_otimizados, listar_tabelas

st.set_page_config(page_title="Explorador SQL", layout="wide")

if "contador_consultas" not in st.session_state:
    st.session_state.contador_consultas = 0

st.header("Explorador de Banco de Dados")

engine = configurar_conexao()

if engine:
    lista = listar_tabelas(engine)
    if lista:
        tabela = st.selectbox("Selecione a tabela:", lista)

        with engine.connect() as conn:
            colunas = pd.read_sql(
                f"SELECT * FROM {tabela} LIMIT 0", conn
            ).columns.tolist()

        cols_sel = st.multiselect("Colunas:", colunas, default=colunas[:3])

        if st.button("Executar Consulta"):
            # Implementação do spinner para feedback de carregamento
            with st.spinner(f"Consultando banco de dados..."):
                st.session_state.contador_consultas += 1
                query = f"SELECT {', '.join(cols_sel)} FROM {tabela} LIMIT 100"

                start = time.time()
                df = buscar_dados_otimizados(query, engine)
                # Delay artificial para percepção do feedback visual
                time.sleep(0.5)

                st.metric("Tempo de Resposta", f"{time.time() - start:.4f}s")
                st.dataframe(df, width="stretch")

            # Notificação de sucesso ao finalizar a tarefa
            st.toast("Consulta finalizada")

        st.markdown("---")
        st.subheader(f"Inserir Registro em {tabela}")

        with st.form("form_registro", clear_on_submit=True):
            novos_dados = {}
            campos_form = colunas[:4]
            cols_layout = st.columns(len(campos_form))

            for i, col_name in enumerate(campos_form):
                with cols_layout[i]:
                    novos_dados[col_name] = st.text_input(f"{col_name}")

            if st.form_submit_button("Salvar no Banco"):
                if any(novos_dados.values()):
                    # Uso do st.status para monitorar o processo de escrita
                    with st.status("Processando inserção...", expanded=True) as status:
                        try:
                            col_names = ", ".join(novos_dados.keys())
                            placeholders = ", ".join(
                                [f":{c}" for c in novos_dados.keys()]
                            )
                            query_insert = text(
                                f"INSERT INTO {tabela} ({col_names}) VALUES ({placeholders})"
                            )

                            with engine.begin() as conn_insert:
                                conn_insert.execute(query_insert, novos_dados)

                            status.update(
                                label="Dados inseridos com sucesso",
                                state="complete",
                                expanded=False,
                            )
                            st.toast("Registro armazenado")
                            st.cache_data.clear()
                            time.sleep(0.8)
                            st.rerun()
                        except Exception as error:
                            status.update(label="Erro na operação", state="error")
                            st.error(f"Detalhes do erro: {error}")
                else:
                    st.warning("Preencha ao menos um campo para prosseguir")
