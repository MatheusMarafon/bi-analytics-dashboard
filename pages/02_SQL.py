import streamlit as st
import pandas as pd
import time
import io
from sqlalchemy import text
from database import configurar_conexao, buscar_dados_otimizados, listar_tabelas

# Configuração da página
st.set_page_config(page_title="Explorador SQL", layout="wide")


# Funções auxiliares de conversão
def converter_para_csv(df):
    return df.to_csv(index=False).encode("utf-8")


def converter_para_excel(df):
    output = io.BytesIO()
    # Certifique-se de ter instalado: pip install xlsxwriter
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Relatorio")
    return output.getvalue()


st.header("Explorador de Banco de Dados")

# Garantia de inicialização do estado (caso acesse a página direto)
if "contador_consultas" not in st.session_state:
    st.session_state.contador_consultas = 0
if "historico_tabelas" not in st.session_state:
    st.session_state.historico_tabelas = []

engine = configurar_conexao()

if engine:
    st.info(f"Consultas realizadas nesta sessão: {st.session_state.contador_consultas}")

    lista = listar_tabelas(engine)
    if lista:
        tabela = st.selectbox("Selecione a tabela:", lista)

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

                # --- SEÇÃO DE EXPORTAÇÃO ---
                st.markdown("###Exportar Resultados")
                col_csv, col_excel = st.columns(2)

                with col_csv:
                    st.download_button(
                        label="Baixar em CSV",
                        data=converter_para_csv(df),
                        file_name=f"extração_{tabela}.csv",
                        mime="text/csv",
                        width="stretch",
                    )

                with col_excel:
                    try:
                        data_excel = converter_para_excel(df)
                        st.download_button(
                            label="Baixar em Excel",
                            data=data_excel,
                            file_name=f"extração_{tabela}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            width="stretch",
                        )
                    except Exception as e:
                        st.error(
                            "Erro ao gerar Excel. Verifique se 'xlsxwriter' está instalado."
                        )

        # Formulário de INSERT Dinâmico
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
                if any(novos_dados.values()):
                    with st.status("Processando...") as status:
                        try:
                            col_names = ", ".join(novos_dados.keys())
                            placeholders = ", ".join(
                                [f":{c}" for c in novos_dados.keys()]
                            )
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
                else:
                    st.warning("Preencha ao menos um campo.")
