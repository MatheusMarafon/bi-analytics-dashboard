import streamlit as st
import pandas as pd
import time
import io
from sqlalchemy import text
from database import configurar_conexao, buscar_dados_otimizados, listar_tabelas

# 1. Configurações Iniciais
st.set_page_config(page_title="Explorador SQL Profissional", layout="wide")


# Funções de Conversão para Exportação
def converter_para_csv(df):
    return df.to_csv(index=False).encode("utf-8")


def converter_para_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Relatorio")
    return output.getvalue()


st.header("Explorador de Banco de Dados")

# Garantia de Session State
if "contador_consultas" not in st.session_state:
    st.session_state.contador_consultas = 0
if "historico_tabelas" not in st.session_state:
    st.session_state.historico_tabelas = []

engine = configurar_conexao()

if engine:
    st.info(f"Consultas realizadas nesta sessão: {st.session_state.contador_consultas}")

    lista = listar_tabelas(engine)

    # Validação: Banco sem tabelas
    if not lista:
        st.warning("Nenhuma tabela encontrada no banco de dados público.")
    else:
        tabela = st.selectbox("Selecione a tabela para explorar:", lista)

        if tabela not in st.session_state.historico_tabelas:
            st.session_state.historico_tabelas.append(tabela)

        # Busca colunas com tratamento de erro
        try:
            with engine.connect() as conn:
                colunas = pd.read_sql(
                    f"SELECT * FROM {tabela} LIMIT 0", conn
                ).columns.tolist()
        except Exception as e:
            st.error(f"Erro ao ler estrutura da tabela: {e}")
            colunas = []

        if colunas:
            cols_sel = st.multiselect(
                "Selecione as colunas:", colunas, default=colunas[:3]
            )

            if st.button("Executar Consulta"):
                with st.spinner(f"Acessando {tabela}..."):
                    st.session_state.contador_consultas += 1
                    query = f"SELECT {', '.join(cols_sel)} FROM {tabela} LIMIT 100"

                    try:
                        df = buscar_dados_otimizados(query, engine)

                        # --- TAREFA: Validação de Dados Vazios ---
                        if df.empty:
                            st.warning(
                                f"A consulta retornou 0 registros para a tabela '{tabela}'."
                            )
                        else:
                            st.toast("Dados carregados!")
                            st.dataframe(df, width="stretch")

                            # --- SEÇÃO DE EXPORTAÇÃO ---
                            st.markdown("### Exportar Relatório")
                            c_csv, c_xls = st.columns(2)

                            with c_csv:
                                st.download_button(
                                    label="Baixar CSV",
                                    data=converter_para_csv(df),
                                    file_name=f"report_{tabela}.csv",
                                    mime="text/csv",
                                )
                            with c_xls:
                                try:
                                    st.download_button(
                                        label="Baixar Excel",
                                        data=converter_para_excel(df),
                                        file_name=f"report_{tabela}.xlsx",
                                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    )
                                except:
                                    st.error(
                                        "Erro ao gerar Excel. Instale 'xlsxwriter'."
                                    )

                    except Exception as e:
                        st.error(f"Erro na execução da query: {e}")

            # --- FORMULÁRIO DE INSERT COM VALIDAÇÃO ---
            st.markdown("---")
            st.subheader(f"Inserir dados em {tabela}")

            with st.form("form_insert", clear_on_submit=True):
                novos_dados = {}
                campos = colunas[:4]
                col_form = st.columns(len(campos))

                for i, nome in enumerate(campos):
                    with col_form[i]:
                        novos_dados[nome] = st.text_input(f"{nome}")

                enviar = st.form_submit_button("Confirmar Inserção")

                if enviar:
                    # Validação: Impedir envio totalmente vazio
                    if not any(novos_dados.values()):
                        st.error(
                            "Preencha pelo menos um campo para realizar a inserção."
                        )
                    else:
                        with st.status("Comunicando com o servidor...") as status:
                            try:
                                col_names = ", ".join(novos_dados.keys())
                                placeholders = ", ".join(
                                    [f":{c}" for c in novos_dados.keys()]
                                )
                                sql_ins = text(
                                    f"INSERT INTO {tabela} ({col_names}) VALUES ({placeholders})"
                                )

                                with engine.begin() as conn:
                                    conn.execute(sql_ins, novos_dados)

                                status.update(
                                    label="Inserção concluída!", state="complete"
                                )
                                st.toast("Sucesso!")
                                st.cache_data.clear()
                                time.sleep(1)
                                st.rerun()
                            except Exception as e:
                                status.update(label="Falha na operação", state="error")
                                st.error(f"Detalhes: {e}")
else:
    st.error(
        "Servidor de banco de dados offline. Verifique as credenciais em secrets.toml."
    )
