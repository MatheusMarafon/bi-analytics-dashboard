import streamlit as st
import pandas as pd
import time
from sqlalchemy import text
from database import configurar_conexao, buscar_dados_otimizados, listar_tabelas

st.set_page_config(page_title="Explorador SQL", layout="wide")
st.header("Explorador SQL Profissional")

# 1. Obtém a conexão centralizada
engine = configurar_conexao()

if engine:
    try:
        # Exibe métrica do Session State (persistente entre páginas)
        st.info(
            f"Consultas realizadas nesta sessão: {st.session_state.contador_consultas}"
        )

        # 2. Busca lista de tabelas (Cacheada)
        lista_tabelas = listar_tabelas(engine)

        if lista_tabelas:
            tabela = st.selectbox("Selecione a tabela para explorar:", lista_tabelas)

            # Monitora histórico no Session State
            if tabela not in st.session_state.historico_tabelas:
                st.session_state.historico_tabelas.append(tabela)

            # 3. Busca colunas para otimização (SELECT específico)
            with engine.connect() as conn:
                colunas_disponiveis = pd.read_sql(
                    f"SELECT * FROM {tabela} LIMIT 0", conn
                ).columns.tolist()

            colunas_selecionadas = st.multiselect(
                "Otimização: Selecione apenas as colunas necessárias:",
                options=colunas_disponiveis,
                default=(
                    colunas_disponiveis[:3]
                    if len(colunas_disponiveis) >= 3
                    else colunas_disponiveis
                ),
            )

            if colunas_selecionadas:
                cols_str = ", ".join(colunas_selecionadas)
                query_final = f"SELECT {cols_str} FROM {tabela} LIMIT 1000"

                # Botão que engatilha o contador de sessão
                if st.button("Executar Consulta"):
                    st.session_state.contador_consultas += 1

                    start_time = time.time()
                    # Uso do @st.cache_data via função importada
                    df_res = buscar_dados_otimizados(query_final, engine)
                    end_time = time.time()

                    # Dashboard de Performance
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Tempo de Resposta", f"{end_time - start_time:.4f}s")
                    c2.metric("Linhas Carregadas", len(df_res))
                    with c3:
                        with engine.connect() as conn:
                            size_res = conn.execute(
                                text(
                                    f"SELECT pg_size_pretty(pg_total_relation_size('{tabela}'))"
                                )
                            ).fetchone()
                            st.metric("Espaço em Disco", size_res[0])

                    st.code(query_final, language="sql")
                    st.dataframe(df_res, use_container_width=True)

            # --- 4. FORMULÁRIO DE INSERT DINÂMICO ---
            st.markdown("---")
            st.subheader(f"Inserir Novo Registro em: {tabela}")

            with st.form("form_registro_multipage", clear_on_submit=True):
                novos_dados = {}
                campos_visiveis = colunas_disponiveis[
                    :4
                ]  # Limita a 4 campos para o layout
                cols_form = st.columns(len(campos_visiveis))

                for i, col_name in enumerate(campos_visiveis):
                    with cols_form[i]:
                        novos_dados[col_name] = st.text_input(f"{col_name}")

                if st.form_submit_button("Salvar no PostgreSQL"):
                    if any(novos_dados.values()):
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

                            st.success("Registro salvo com sucesso!")
                            st.cache_data.clear()  # Limpa cache para atualizar a visualização
                            st.rerun()
                        except Exception as error:
                            st.error(f"Erro no INSERT: {error}")
                    else:
                        st.warning("Preencha ao menos um campo.")

            # Histórico no rodapé
            if st.session_state.historico_tabelas:
                st.caption(
                    f"Histórico desta sessão: {', '.join(st.session_state.historico_tabelas)}"
                )

        else:
            st.warning("Nenhuma tabela encontrada no banco.")

    except Exception as e:
        st.error(f"Erro na página SQL: {e}")
else:
    st.error("Falha ao carregar o Engine de conexão.")
