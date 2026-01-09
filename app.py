import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
from sqlalchemy import create_engine, text

# Configurações da página
st.set_page_config(page_title="Estudo Dashboard", layout="wide")

# --- Dia 02: Sidebar (Layout Avançado) ---
st.sidebar.header("Filtros do Dashboard")

st.sidebar.subheader("Localização")
cidade = st.sidebar.selectbox(
    "Escolha a cidade:",
    options=["São Paulo", "Rio de Janeiro", "Curitiba", "Belo Horizonte"],
)

st.sidebar.subheader("Categorias")
tecnologias = st.sidebar.multiselect(
    "Selecione as tecnologias",
    options=[
        "Python",
        "SQL",
        "HTML",
        "CSS",
        "React",
        "React Native",
        "JavaScript",
        "Java",
        "C",
        "C#",
    ],
    default=["Python", "SQL"],
)

st.sidebar.subheader("Experiência")
anos_xp = st.sidebar.slider("Anos de experiência na área:", 0, 20, 1)

st.sidebar.subheader("Período de Análise")
data_range = st.sidebar.date_input(
    "Selecione o intervalo:",
    value=(pd.to_datetime("2025-01-01"), pd.to_datetime("2025-12-31")),
)

# --- Dia 01 (Semana 4): Funções com Cache ---


@st.cache_data(ttl=600)  # O cache expira em 10 minutos (600 segundos)
def buscar_dados_otimizados(query_string, _engine):
    """
    Executa a query e armazena o resultado em cache.
    O '_' no engine diz ao Streamlit para não tentar 'hashear' o objeto de conexão.
    """
    with _engine.connect() as conn:
        df = pd.read_sql(query_string, conn)
    return df


@st.cache_data
def listar_tabelas(_engine):
    query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
    with _engine.connect() as conn:
        return pd.read_sql(query, conn)["table_name"].tolist()


# --- Dia 02 (Semana 4): Cache de Recurso (Conexão) ---


@st.cache_resource
def configurar_conexao():
    """
    Cria e armazena o engine de conexão com o banco.
    O @st.cache_resource garante que o engine seja criado apenas UMA vez,
    evitando abrir centenas de conexões desnecessárias com o Postgres.
    """
    try:
        db = st.secrets["postgres"]
        conn_url = (
            f"postgresql://{db['user']}@{db['host']}:{db['port']}/{db['database']}"
        )
        return create_engine(conn_url)
    except Exception as e:
        st.error(f"Erro ao configurar conexão global: {e}")
        return None


# Chamada global para obter o engine (fora das abas)
engine = configurar_conexao()

# --- Dia 04 e 05: Layout e Gráficos ---
st.title("Estrutura de Layout Avançada")

(
    tab_home,
    tab_dados,
    tab_filtros,
    tab_graficos,
    tab_plotly,
    tab_tendencia,
    tab_comparativo,
    tab_mapa,
    tab_design,
    tab_sql,
) = st.tabs(
    [
        "Início",
        "Visualização de Dados",
        "Análise de Filtros",
        "Gráficos",
        "Plotly",
        "Tendências Temporais",
        "Comparativos",
        "Distribuição Geográfica",
        "Design Final",
        "Conexão SQL",
    ]
)

with tab_home:
    st.header("Hello, World!")
    st.write("Bem-vindo ao meu Dashboard de BI com Streamlit")
    st.info("Navegue pelas abas acima para ver a evolução do projeto.")

with tab_dados:
    st.header("Dia 03: Display de Dados")

    dados_vendas = {
        "Produto": ["Teclado", "Mouse", "Monitor", "Notebook"],
        "Preço": [150.50, 80.00, 900.00, 4500.00],
        "Estoque": [15, 30, 10, 5],
    }
    df = pd.DataFrame(dados_vendas)

    col_esq, col_dir = st.columns(2)
    with col_esq:
        st.subheader("Interativo (st.dataframe)")
        st.dataframe(df, width="stretch")
    with col_dir:
        st.subheader("Estático (st.table)")
        st.table(df)

with tab_filtros:
    st.header("Análise de Filtros")

    m1, m2, m3 = st.columns(3)
    m1.metric("Cidade", cidade)
    m2.metric("XP", f"{anos_xp} anos")
    m3.metric("Tecnologias", len(tecnologias))

    st.markdown("---")

    col_info1, col_info2 = st.columns([1, 1])
    with col_info1:
        st.success(f"**Tecnologias focadas:** {', '.join(tecnologias)}")

    with col_info2:
        if anos_xp > 5:
            st.write("Perfil com experiência avançada detectado!")
        else:
            st.write("Perfil em desenvolvimento de carreira.")

# --- Dia 05: Primeiro Gráficos ---
with tab_graficos:
    st.header("Gráficos Básicos Interativos")

    # Criando dados fictícios que reagem ao slider de XP
    chart_data = pd.DataFrame(
        (
            np.random.randn(anos_xp + 1, len(tecnologias))
            if tecnologias
            else np.random.randn(anos_xp + 1, 1)
        ),
        columns=tecnologias if tecnologias else ["Geral"],
    )

    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        st.subheader("Evolução (Line Chart)")
        st.line_chart(chart_data)

    with col_graf2:
        st.subheader("Distribuição (Bar Chart)")
        st.bar_chart(chart_data)

    st.caption(
        f"Dados gerados aleatoriamente para representar {anos_xp} pontos de dados em {cidade}."
    )

with tab_plotly:
    st.header("Gráficos Customizados com Plotly Express")

    # Dados para o gráfico baseados nos filtros
    df_plotly = pd.DataFrame(
        {
            "Tecnologia": tecnologias if tecnologias else ["Nenhuma"],
            "Demanda": (
                np.random.randint(10, 100, size=len(tecnologias))
                if tecnologias
                else [0]
            ),
            "Mercado": (
                np.random.randint(1000, 5000, size=len(tecnologias))
                if tecnologias
                else [0]
            ),
        }
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Gráfico de Barras Plotly")
        fig_bar = px.bar(
            df_plotly,
            x="Tecnologia",
            y="Demanda",
            color="Tecnologia",
            title=f"Demanda em {cidade}",
            template="plotly_dark",
        )
        st.plotly_chart(fig_bar, width="stretch")

    with col2:
        st.subheader("Relação Demanda vs Mercado")
        fig_scatter = px.scatter(
            df_plotly,
            x="Demanda",
            y="Mercado",
            size="Demanda",
            color="Tecnologia",
            hover_name="Tecnologia",
        )
        st.plotly_chart(fig_scatter, width="stretch")

with tab_tendencia:
    st.header("Análise de Tendência Temporal")

    # Gerando dados temporais fictícios
    datas = pd.date_range(start="2025-01-01", end="2025-12-31", freq="ME")
    df_vendas = pd.DataFrame(
        {
            "Data": datas,
            "Vendas": np.random.randint(100, 500, size=len(datas)),
            "Meta": np.random.randint(200, 400, size=len(datas)),
        }
    )

    # Filtrando os dados com base na Sidebar
    if len(data_range) == 2:
        start_date, end_date = data_range
        mask = (df_vendas["Data"] >= pd.to_datetime(start_date)) & (
            df_vendas["Data"] <= pd.to_datetime(end_date)
        )
        df_filtrado = df_vendas.loc[mask]

        fig_linha = px.line(
            df_filtrado,
            x="Data",
            y=["Vendas", "Meta"],
            title=f"Evolução de Performance em {cidade}",
            markers=True,
            template="plotly_white",
        )
        st.plotly_chart(fig_linha, width="stretch")
    else:
        st.warning("Por favor, selecione as datas de início e fim.")

with tab_comparativo:
    st.header("Gráficos de Comparação e Fluxo")

    col_comp1, col_comp2 = st.columns(2)

    with col_comp1:
        st.subheader("Comparativo por Tecnologia")
        # Criando dados para barras agrupadas
        df_comp = pd.DataFrame(
            {
                "Tecnologia": tecnologias * 2 if tecnologias else ["Geral"] * 2,
                "Valor": (
                    np.random.randint(40, 100, size=len(tecnologias) * 2)
                    if tecnologias
                    else [50, 60]
                ),
                "Tipo": (
                    ["Realizado"] * len(tecnologias) + ["Previsto"] * len(tecnologias)
                    if tecnologias
                    else ["Realizado", "Previsto"]
                ),
            }
        )

        fig_agrupado = px.bar(
            df_comp,
            x="Tecnologia",
            y="Valor",
            color="Tipo",
            barmode="group",
            title="Realizado vs Previsto",
        )
        st.plotly_chart(fig_agrupado, width="stretch")

    with col_comp2:
        st.subheader("Funil de Contratação")
        # Dados para o gráfico de funil
        df_funil = pd.DataFrame(
            {
                "Etapa": [
                    "Visualizações",
                    "Candidaturas",
                    "Entrevistas",
                    "Propostas",
                    "Contratações",
                ],
                "Quantidade": [1000, 450, 120, 30, 10],
            }
        )

        fig_funil = px.funnel(
            df_funil, x="Quantidade", y="Etapa", title="Funil de Recrutamento Tech"
        )
        st.plotly_chart(fig_funil, width="stretch")

with tab_mapa:
    st.header("Visualização Geoespacial")

    # Coordenadas aproximadas das cidades da sua sidebar
    coords = {
        "São Paulo": [-23.55, -46.63],
        "Rio de Janeiro": [-22.90, -43.17],
        "Curitiba": [-25.42, -49.27],
        "Belo Horizonte": [-19.91, -43.93],
    }

    lat_base, lon_base = coords.get(cidade, [-23.55, -46.63])

    # Gerando pontos aleatórios ao redor da cidade selecionada
    df_mapa = pd.DataFrame(
        np.random.randn(100, 2) / [50, 50] + [lat_base, lon_base],
        columns=["lat", "lon"],
    )

    st.subheader(f"Densidade de Talentos em {cidade}")
    # Comando nativo do Streamlit para mapas rápidos
    st.map(df_mapa)

    st.markdown("---")
    st.subheader("Mapa Detalhado (Plotly)")

    # Mapa mais profissional usando Plotly
    fig_mapa = px.scatter_map(
        df_mapa,
        lat="lat",
        lon="lon",
        zoom=10,
        height=400,
        title=f"Distribuição de Profissionais - {cidade}",
    )
    st.plotly_chart(fig_mapa, width="stretch")

with tab_design:
    st.header("Identidade Visual e Customização")
    st.info(
        """
    **Diferença entre Caches:**
    - **cache_data:** Armazena o conteúdo (ex: o resultado da tabela de vendas).
    - **cache_resource:** Armazena o conector (ex: o túnel de acesso ao Postgres).
    """
    )
    # Criando dados para o exemplo de design
    df_design = pd.DataFrame(
        {
            "Métrica": ["Performance", "Engajamento", "Retenção", "Qualidade"],
            "Valor": [85, 92, 78, 88],
        }
    )

    # Definindo uma paleta de cores customizada (Hex Colors)
    minha_paleta = ["#003f5c", "#7a5195", "#ef5675", "#ffa600"]

    fig_design = px.bar(
        df_design,
        x="Métrica",
        y="Valor",
        color="Métrica",
        color_discrete_sequence=minha_paleta,
        title="KPIs de Engenharia de Dados",
    )

    # Customização Profissional via update_layout e update_traces
    fig_design.update_layout(
        title_font_size=24,
        xaxis_title="Categorias de BI",
        yaxis_title="Percentual (%)",
        legend_title="Indicadores",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#888",
        margin=dict(l=20, r=20, t=60, b=20),
    )

    fig_design.update_traces(
        marker_line_color="rgb(8,48,107)", marker_line_width=1.5, opacity=0.8
    )

    st.plotly_chart(fig_design, width="stretch")

    st.success("Design finalizado com identidade visual consistente!")

with tab_sql:
    st.header("Explorador de Dados SQL (Arquitetura Pro)")

    # O 'engine' agora vem da função cacheada @st.cache_resource no topo do script
    if engine is not None:
        try:
            # 1. Busca lista de tabelas usando CACHE
            lista_tabelas = listar_tabelas(engine)

            if lista_tabelas:
                tabela = st.selectbox(
                    "Selecione a tabela para explorar:", lista_tabelas
                )

                # 2. Busca colunas da tabela selecionada (operação rápida)
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
                    # Preparando a Query
                    cols_str = ", ".join(colunas_selecionadas)
                    query_final = f"SELECT {cols_str} FROM {tabela} WHERE 1=1"

                    if "cidade" in colunas_disponiveis:
                        query_final += f" AND cidade = '{cidade}'"

                    # 3. Execução com medição de tempo e CACHE DE DADOS
                    start_time = time.time()
                    df_res = buscar_dados_otimizados(query_final, engine)
                    end_time = time.time()

                    # Dashboard de Performance
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Tempo de Resposta", f"{end_time - start_time:.4f}s")
                    c2.metric("Linhas", len(df_res))
                    with c3:
                        with engine.connect() as conn:
                            size_res = conn.execute(
                                text(
                                    f"SELECT pg_size_pretty(pg_total_relation_size('{tabela}'))"
                                )
                            ).fetchone()
                            st.metric("Espaço em Disco", size_res[0])

                    st.code(query_final, language="sql")
                    st.dataframe(df_res, width="stretch")

                # 4. Formulário CRUD Dinâmico
                st.markdown("---")
                st.subheader(f"Inserir Registro em {tabela}")

                with st.form("form_registro_final", clear_on_submit=True):
                    novos_dados = {}
                    # Exibe inputs apenas para as colunas selecionadas ou as 4 primeiras
                    campos_form = colunas_disponiveis[:4]
                    cols_form = st.columns(len(campos_form))

                    for i, col_name in enumerate(campos_form):
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

                                st.success(
                                    "Registro salvo! Limpando cache para atualizar dados..."
                                )
                                st.cache_data.clear()  # Garante que o BI mostre o dado novo
                                st.rerun()  # Recarrega a página para atualizar o dataframe acima
                            except Exception as error:
                                st.error(f"Erro no INSERT: {error}")
                        else:
                            st.warning("Preencha ao menos um campo.")
            else:
                st.warning("Nenhuma tabela encontrada no schema 'public'.")

        except Exception as e:
            st.error(f"Erro durante a exploração: {e}")
    else:
        st.error("Engine de conexão não disponível. Verifique os Secrets.")
