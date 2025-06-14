import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Configuração da página Streamlit ---
st.set_page_config(layout="wide", page_title="Dashboard de Análise de Jogos (Plotly com Abas)")

st.title("🎮 Dashboard de Análise de Jogos com Plotly (Com Abas)")
st.markdown("Explore dados sobre lançamentos, gêneros, desenvolvedores e preços de jogos.")

# --- Carregar e Preparar os Dados (Diretamente no Streamlit) ---
@st.cache_data # Decorador para cachear os dados e evitar recarregamento a cada interação
def load_and_preprocess_data():
    """Carrega o dataset e realiza todas as etapas de pré-processamento."""
    try:
        df = pd.read_csv('DB_completo.csv')
    except FileNotFoundError:
        st.error("ERRO: DB_completo.csv não encontrado. Por favor, certifique-se de que o arquivo está na mesma pasta do script.")
        st.stop()

    # Aplicando: df.drop_duplicates(inplace=True)
    df.drop_duplicates(inplace=True)

    # Processamento de Gêneros
    genre_columns = [col for col in df.columns if col.startswith('genre_')]
    df['genre'] = df.apply(
        lambda row: [col.replace('genre_', '') for col in genre_columns if row[col]],
        axis=1
    )
    df['genre'] = df['genre'].apply(
        lambda x: x if x else ['Desconhecido']
    )

    # Processamento de Datas
    df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce').fillna(0).astype(int)
    df['release_month'] = pd.to_numeric(df['release_month'], errors='coerce').fillna(1).astype(int)
    df['release_date'] = pd.to_datetime(
        df['release_year'].astype(str) + '-' +
        df['release_month'].astype(str).str.zfill(2) + '-01',
        errors='coerce'
    )
    df.dropna(subset=['release_date'], inplace=True)

    # Explodir o DataFrame para análise por gênero (se necessário)
    df_genres_exploded = df.explode('genre')

    # Definir Períodos da Pandemia
    pre_pandemic_end = pd.Timestamp('2020-03-31')
    pandemic_start = pd.Timestamp('2020-04-01')
    pandemic_end = pd.Timestamp('2022-03-31')
    post_pandemic_start = pd.Timestamp('2022-04-01')

    def assign_period_with_dates(date):
        if date < pandemic_start:
            return 'Pré-Pandemia'
        elif pandemic_start <= date <= pandemic_end:
            return 'Durante a Pandemia'
        elif date >= post_pandemic_start:
            return 'Pós-Pandemia'
        return 'Desconhecido'

    df_genres_exploded['periodo'] = df_genres_exploded['release_date'].apply(assign_period_with_dates)
    df['periodo'] = df['release_date'].apply(assign_period_with_dates)

    # Garantir colunas de preço numéricas
    df['preco_dolar'] = pd.to_numeric(df['preco_dolar'], errors='coerce')
    df['preco_euro'] = pd.to_numeric(df['preco_euro'], errors='coerce')
    df.dropna(subset=['preco_dolar', 'preco_euro'], inplace=True)

    df_genres_exploded['preco_dolar'] = pd.to_numeric(df_genres_exploded['preco_dolar'], errors='coerce')
    df_genres_exploded['preco_euro'] = pd.to_numeric(df_genres_exploded['preco_euro'], errors='coerce')
    df_genres_exploded.dropna(subset=['preco_dolar', 'preco_euro'], inplace=True)

    return df, df_genres_exploded

df, df_genres_exploded = load_and_preprocess_data()
st.sidebar.success("Dados carregados e pré-processados com sucesso!")


# --- Adicionar Filtros na Barra Lateral ---
st.sidebar.header("Filtros de Dados")

# Seleção de Plataforma
all_platforms = sorted(df['platform'].unique().tolist())
selected_platforms = st.sidebar.multiselect(
    'Selecione a(s) Plataforma(s):',
    options=all_platforms,
    default=all_platforms
)

# Seleção de Período da Pandemia
all_periods = ['Pré-Pandemia', 'Durante a Pandemia', 'Pós-Pandemia', 'Desconhecido']
selected_periods = st.sidebar.multiselect(
    'Selecione o(s) Período(s):',
    options=all_periods,
    default=all_periods
)

# Seleção de Gênero
all_genres = sorted(df_genres_exploded['genre'].unique().tolist())
selected_genres = st.sidebar.multiselect(
    'Selecione o(s) Gênero(s):',
    options=all_genres,
    default=all_genres
)

# Filtro de Ano (Range Slider)
min_year, max_year = int(df['release_year'].min()), int(df['release_year'].max())
year_range = st.sidebar.slider(
    'Selecione o Intervalo de Anos:',
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# --- Aplicar Filtros ao DataFrame ---
df_filtered = df[
    df['platform'].isin(selected_platforms) &
    df['periodo'].isin(selected_periods) &
    (df['release_year'] >= year_range[0]) &
    (df['release_year'] <= year_range[1])
]

# Filtrar o DataFrame de gêneros explodidos para gráficos baseados em gênero
df_genres_filtered = df_genres_exploded[
    df_genres_exploded['platform'].isin(selected_platforms) &
    df_genres_exploded['periodo'].isin(selected_periods) &
    df_genres_exploded['genre'].isin(selected_genres) &
    (df_genres_exploded['release_year'] >= year_range[0]) &
    (df_genres_exploded['release_year'] <= year_range[1])
]


# --- Geração e Exibição dos Gráficos com Plotly.express em ABAS ---
# Criar as abas
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Gêneros por Período",
    "Lançamentos Temporais",
    "Gêneros por Plataforma",
    "Top Desenvolvedores",
    "Preços por Gênero/Plataforma"
])

with tab1:
    st.header("1. Gêneros Mais Lançados por Plataforma e Período")
    df_chart1 = df_genres_filtered.groupby(['periodo', 'platform', 'genre']).size().reset_index(name='count')
    period_order = ['Pré-Pandemia', 'Durante a Pandemia', 'Pós-Pandemia', 'Desconhecido']
    df_chart1['periodo'] = pd.Categorical(df_chart1['periodo'], categories=period_order, ordered=True)
    df_chart1.sort_values(by=['periodo', 'platform', 'count'], ascending=[True, True, False], inplace=True)

    if not df_chart1.empty:
        fig1 = px.bar(
            df_chart1,
            x='count',
            y='genre',
            color='platform',
            facet_col='periodo',
            facet_col_wrap=2,
            title='Gêneros Mais Lançados por Plataforma e Período',
            labels={'count': 'Número de Lançamentos', 'genre': 'Gênero'},
            orientation='h',
            height=500
        )
        fig1.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Nenhum dado para exibir para o gráfico de Gêneros por Plataforma e Período com os filtros selecionados.")

with tab2:
    st.header("2. Distribuição Temporal de Lançamentos por Plataforma")
    df_chart2 = df_filtered.groupby(['platform', pd.Grouper(key='release_date', freq='M')]).size().reset_index(name='count')
    df_chart2.rename(columns={'release_date': 'release_month_year'}, inplace=True)

    if not df_chart2.empty:
        fig2 = px.line(
            df_chart2,
            x='release_month_year',
            y='count',
            color='platform',
            title='Distribuição Temporal de Lançamentos por Plataforma',
            labels={'release_month_year': 'Data de Lançamento', 'count': 'Número de Jogos Lançados'},
            height=450
        )
        fig2.update_xaxes(
            dtick="M12",
            tickformat="%Y",
            showgrid=True
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Nenhum dado para exibir para o gráfico de Distribuição Temporal com os filtros selecionados.")

with tab3:
    st.header("3. Gêneros Dominantes por Plataforma")
    df_chart3 = df_genres_filtered.groupby(['platform', 'genre']).size().reset_index(name='count')

    if not df_chart3.empty:
        fig3 = px.bar(
            df_chart3,
            x='count',
            y='genre',
            color='platform',
            facet_col='platform',
            facet_col_wrap=2,
            title='Gêneros Dominantes por Plataforma',
            labels={'count': 'Número de Jogos', 'genre': 'Gênero'},
            orientation='h',
            height=500
        )
        fig3.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Nenhum dado para exibir para o gráfico de Gêneros Dominantes com os filtros selecionados.")

with tab4:
    st.header("4. Top 10 Desenvolvedores por Lançamentos e Gênero")
    developer_total_counts = df_filtered.groupby('developers').size().reset_index(name='total_games')
    top_developers = developer_total_counts.sort_values('total_games', ascending=False).head(10)['developers'].tolist()

    df_chart4 = df_genres_filtered[df_genres_filtered['developers'].isin(top_developers)]
    df_chart4 = df_chart4.groupby(['developers', 'genre']).size().reset_index(name='count')

    if not df_chart4.empty:
        fig4 = px.bar(
            df_chart4,
            x='count',
            y='genre',
            color='genre',
            facet_col='developers',
            facet_col_wrap=3,
            title='Top 10 Desenvolvedores por Lançamentos e Gênero',
            labels={'count': 'Número de Lançamentos', 'genre': 'Gênero', 'developers': 'Desenvolvedor'},
            orientation='h',
            height=600
        )
        fig4.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("Nenhum dado para exibir para o gráfico de Top Desenvolvedores com os filtros selecionados.")

with tab5:
    st.header("5. Distribuição de Preços (Dólar) por Plataforma e Gênero")
    df_chart5 = df_genres_filtered[['platform', 'genre', 'preco_dolar']]

    if not df_chart5.empty:
        fig5 = px.box(
            df_chart5,
            x='platform',
            y='preco_dolar',
            color='genre',
            title='Distribuição de Preços (Dólar) por Plataforma e Gênero',
            labels={'platform': 'Plataforma', 'preco_dolar': 'Preço em Dólar', 'genre': 'Gênero'},
            log_y=True,
            height=500
        )
        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.info("Nenhum dado para exibir para o gráfico de Preços com os filtros selecionados.")


st.sidebar.header("Sobre este Dashboard")
st.sidebar.info(
    "Este dashboard interativo permite explorar dados de jogos, incluindo tendências de lançamento, "
    "preferências de gênero, atividades de desenvolvedores e distribuição de preços. "
    "Os dados são filtrados em tempo real pelas seleções na barra lateral."
)