import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 

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
    value=(pd.to_datetime("2025-01-01"), pd.to_datetime("2025-12-31"))
)

# --- Dia 04 e 05: Layout e Gráficos --- 
st.title("Estrutura de Layout Avançada")

tab_home, tab_dados, tab_filtros, tab_graficos, tab_plotly, tab_tendencia, tab_comparativo = st.tabs(
    ["Início", "Visualização de Dados", "Análise de Filtros", "Gráficos", "Plotly", "Tendências Temporais", "Comparativos"]
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
        np.random.randn(anos_xp + 1, len(tecnologias)) if tecnologias else np.random.randn(anos_xp + 1, 1),
        columns = tecnologias if tecnologias else ["Geral"] 
    )

    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        st.subheader("Evolução (Line Chart)")
        st.line_chart(chart_data)
    
    with col_graf2:
        st.subheader("Distribuição (Bar Chart)")
        st.bar_chart(chart_data)
    
    st.caption(f"Dados gerados aleatoriamente para representar {anos_xp} pontos de dados em {cidade}.")

with tab_plotly:
    st.header("Gráficos Customizados com Plotly Express")
    
    # Dados para o gráfico baseados nos filtros
    df_plotly = pd.DataFrame({
        "Tecnologia": tecnologias if tecnologias else ["Nenhuma"],
        "Demanda": np.random.randint(10, 100, size=len(tecnologias)) if tecnologias else [0],
        "Mercado": np.random.randint(1000, 5000, size=len(tecnologias)) if tecnologias else [0]
    })

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Gráfico de Barras Plotly")
        fig_bar = px.bar(
            df_plotly, 
            x="Tecnologia", 
            y="Demanda", 
            color="Tecnologia",
            title=f"Demanda em {cidade}",
            template="plotly_dark"
        )
        st.plotly_chart(fig_bar, width='stretch')

    with col2:
        st.subheader("Relação Demanda vs Mercado")
        fig_scatter = px.scatter(
            df_plotly,
            x="Demanda",
            y="Mercado",
            size="Demanda",
            color="Tecnologia",
            hover_name="Tecnologia"
        )
        st.plotly_chart(fig_scatter, width='stretch')

with tab_tendencia:
    st.header("Análise de Tendência Temporal")
    
    # Gerando dados temporais fictícios
    datas = pd.date_range(start="2025-01-01", end="2025-12-31", freq="M")
    df_vendas = pd.DataFrame({
        "Data": datas,
        "Vendas": np.random.randint(100, 500, size=len(datas)),
        "Meta": np.random.randint(200, 400, size=len(datas))
    })

    # Filtrando os dados com base na Sidebar
    if len(data_range) == 2:
        start_date, end_date = data_range
        mask = (df_vendas["Data"] >= pd.to_datetime(start_date)) & (df_vendas["Data"] <= pd.to_datetime(end_date))
        df_filtrado = df_vendas.loc[mask]

        fig_linha = px.line(
            df_filtrado, 
            x="Data", 
            y=["Vendas", "Meta"],
            title=f"Evolução de Performance em {cidade}",
            markers=True,
            template="plotly_white"
        )
        st.plotly_chart(fig_linha, width='stretch')
    else:
        st.warning("Por favor, selecione as datas de início e fim.")

with tab_comparativo:
    st.header("Gráficos de Comparação e Fluxo")

    col_comp1, col_comp2 = st.columns(2)

    with col_comp1:
        st.subheader("Comparativo por Tecnologia")
        # Criando dados para barras agrupadas
        df_comp = pd.DataFrame({
            "Tecnologia": tecnologias * 2 if tecnologias else ["Geral"] * 2,
            "Valor": np.random.randint(40, 100, size=len(tecnologias)*2) if tecnologias else [50, 60],
            "Tipo": ["Realizado"] * len(tecnologias) + ["Previsto"] * len(tecnologias) if tecnologias else ["Realizado", "Previsto"]
        })
        
        fig_agrupado = px.bar(
            df_comp, 
            x="Tecnologia", 
            y="Valor", 
            color="Tipo", 
            barmode="group",
            title="Realizado vs Previsto"
        )
        st.plotly_chart(fig_agrupado, width='stretch')

    with col_comp2:
        st.subheader("Funil de Contratação")
        # Dados para o gráfico de funil
        df_funil = pd.DataFrame({
            "Etapa": ["Visualizações", "Candidaturas", "Entrevistas", "Propostas", "Contratações"],
            "Quantidade": [1000, 450, 120, 30, 10]
        })
        
        fig_funil = px.funnel(
            df_funil, 
            x="Quantidade", 
            y="Etapa",
            title="Funil de Recrutamento Tech"
        )
        st.plotly_chart(fig_funil, width='stretch')