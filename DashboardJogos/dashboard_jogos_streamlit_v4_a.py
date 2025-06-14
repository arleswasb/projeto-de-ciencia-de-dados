import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Configuração da página Streamlit ---
st.set_page_config(layout="wide", page_title="Dashboard de Análise de Jogos (Sunburst)")

st.title("🎮 Dashboard de Análise de Jogos com Plotly (Sunburst)")
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


# --- Adicionar Filtros Globais na Barra Lateral ---
st.sidebar.header("Filtros Globais")

# Seleção de Plataforma (GLOBAL)
all_platforms = sorted(df['platform'].unique().tolist())
selected_platforms_global = st.sidebar.multiselect(
    'Plataforma(s):',
    options=all_platforms,
    default=all_platforms,
    key='global_platforms'
)

# Seleção de Gênero (GLOBAL)
all_genres_global = sorted(df_genres_exploded['genre'].unique().tolist())
selected_genres_global = st.sidebar.multiselect(
    'Gênero(s):',
    options=all_genres_global,
    default=all_genres_global,
    key='global_genres'
)

# --- Aplicar Filtros Globais ao DataFrame ---
# Estes DataFrames serão a base para os filtros específicos de cada aba
df_base_filtered_global = df[
    df['platform'].isin(selected_platforms_global)
]

df_genres_base_filtered_global = df_genres_exploded[
    df_genres_exploded['platform'].isin(selected_platforms_global) &
    df_genres_exploded['genre'].isin(selected_genres_global)
]


# --- Geração e Exibição dos Gráficos com Plotly.express em ABAS ---
# Criar as abas
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([ # Adicionado tab6
    "Gêneros por Período",
    "Lançamentos Temporais",
    "Gêneros por Plataforma",
    "Top Desenvolvedores",
    "Preços por Gênero/Plataforma",
    "Visão Hierárquica (Sunburst)" # Novo rótulo da aba
])

# --- TAB 1: Gêneros por Período (Gráficos Individuais em Grade) ---
with tab1:
    st.header("1. Gêneros Mais Lançados por Plataforma e Período")

    # Filtros específicos para esta aba (Período da Pandemia e Ano)
    st.subheader("Filtros Adicionais para esta Análise")
    col_filters_tab1_1, col_filters_tab1_2 = st.columns(2)
    with col_filters_tab1_1:
        all_periods_tab1 = ['Pré-Pandemia', 'Durante a Pandemia', 'Pós-Pandemia', 'Desconhecido']
        selected_periods_tab1 = st.multiselect(
            'Período(s) da Pandemia:', 
            options=all_periods_tab1, 
            default=all_periods_tab1, 
            key='tab1_periods'
        )
    with col_filters_tab1_2:
        min_year_tab1, max_year_tab1 = int(df_genres_base_filtered_global['release_year'].min()), int(df_genres_base_filtered_global['release_year'].max())
        year_range_tab1 = st.slider(
            'Intervalo de Anos:', 
            min_value=min_year_tab1, 
            max_value=max_year_tab1,
            value=(min_year_tab1, max_year_tab1), 
            key='tab1_years'
        )

    st.divider()  # Linha divisória

    # Aplicar filtros (globais + específicos da aba)
    df_chart1_filtered = df_genres_base_filtered_global[
        df_genres_base_filtered_global['periodo'].isin(selected_periods_tab1) &
        (df_genres_base_filtered_global['release_year'] >= year_range_tab1[0]) &
        (df_genres_base_filtered_global['release_year'] <= year_range_tab1[1])
    ]

    # Criar o DataFrame agregado
    df_chart1 = df_chart1_filtered.groupby(['periodo', 'platform', 'genre']).size().reset_index(name='count')
    period_order = ['Pré-Pandemia', 'Durante a Pandemia', 'Pós-Pandemia', 'Desconhecido']
    df_chart1['periodo'] = pd.Categorical(df_chart1['periodo'], categories=period_order, ordered=True)
    df_chart1.sort_values(by=['periodo', 'platform', 'count'], ascending=[True, True, False], inplace=True)

    if not df_chart1.empty:
        # --- DISPOSIÇÃO EM GRADE (2x2) ---
        st.subheader("Distribuição por Período")
        
        # Criar colunas para a grade
        col1, col2 = st.columns(2)
        cols = [col1, col2]
        
        # Iterar sobre os períodos e plotar em grade
        for i, periodo in enumerate(period_order):
            if periodo in selected_periods_tab1:  # Só plota se o período estiver selecionado
                df_periodo = df_chart1[df_chart1['periodo'] == periodo]
                
                with cols[i % 2]:  # Alterna entre col1 e col2
                    fig = px.bar(
                        df_periodo,
                        x='count',
                        y='genre',
                        color='platform',
                        title=f'Gêneros em {periodo}',
                        labels={'count': 'Nº de Lançamentos', 'genre': 'Gênero'},
                        orientation='h',
                        height=500,  # Altura fixa para uniformidade
                        width=400    # Largura controlada
                    )
                    
                    # Ajustes de layout
                    fig.update_layout(
                        yaxis={'categoryorder': 'total ascending'},
                        margin=dict(l=100, r=50, b=100, t=80),
                        showlegend=(i == 0)  # Mostra legenda apenas no primeiro gráfico
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                # Adiciona um divisor após cada linha (2 gráficos)
                if i % 2 == 1 and i < len(period_order) - 1:
                    st.divider()
    else:
        st.info("Nenhum dado encontrado para os filtros selecionados.")


# --- TAB 2: Lançamentos Temporais ---
with tab2:
    st.header("2. Distribuição Temporal de Lançamentos por Plataforma")

    # Filtros específicos para esta aba (Período da Pandemia e Ano)
    st.subheader("Filtros Adicionais para esta Análise")
    col_filters_tab2_1, col_filters_tab2_2 = st.columns(2)
    with col_filters_tab2_1:
        all_periods_tab2 = ['Pré-Pandemia', 'Durante a Pandemia', 'Pós-Pandemia', 'Desconhecido']
        selected_periods_tab2 = st.multiselect(
            'Período(s) da Pandemia:', options=all_periods_tab2, default=all_periods_tab2, key='tab2_periods'
        )
    with col_filters_tab2_2:
        min_year_tab2, max_year_tab2 = int(df_base_filtered_global['release_year'].min()), int(df_base_filtered_global['release_year'].max())
        year_range_tab2 = st.slider(
            'Intervalo de Anos:', min_value=min_year_tab2, max_value=max_year_tab2,
            value=(min_year_tab2, max_year_tab2), key='tab2_years'
        )

    # Aplicar filtros (globais + específicos da aba)
    df_chart2_filtered = df_base_filtered_global[
        df_base_filtered_global['periodo'].isin(selected_periods_tab2) &
        (df_base_filtered_global['release_year'] >= year_range_tab2[0]) &
        (df_base_filtered_global['release_year'] <= year_range_tab2[1])
    ]

    # Criar o DataFrame agregado
    df_chart2 = df_chart2_filtered.groupby(['platform', pd.Grouper(key='release_date', freq='M')]).size().reset_index(name='count')
    df_chart2.rename(columns={'release_date': 'release_month_year'}, inplace=True)

    if not df_chart2.empty:
        fig2 = px.line(
            df_chart2, x='release_month_year', y='count', color='platform',
            title='Distribuição Temporal de Lançamentos por Plataforma',
            labels={'release_month_year': 'Data de Lançamento', 'count': 'Número de Jogos Lançados'},
            height=450
        )
        fig2.update_xaxes(dtick="M12", tickformat="%Y", showgrid=True)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Nenhum dado para exibir para o gráfico de Distribuição Temporal com os filtros selecionados.")


# --- TAB 3: Gêneros Dominantes por Plataforma ---
with tab3:
    st.header("3. Gêneros Dominantes por Plataforma")

    # Filtros específicos para esta aba (Período da Pandemia e Ano)
    st.subheader("Filtros Adicionais para esta Análise")
    col_filters_tab3_1, col_filters_tab3_2 = st.columns(2)
    with col_filters_tab3_1:
        all_periods_tab3 = ['Pré-Pandemia', 'Durante a Pandemia', 'Pós-Pandemia', 'Desconhecido']
        selected_periods_tab3 = st.multiselect(
            'Período(s) da Pandemia:', options=all_periods_tab3, default=all_periods_tab3, key='tab3_periods'
        )
    with col_filters_tab3_2:
        min_year_tab3, max_year_tab3 = int(df_genres_base_filtered_global['release_year'].min()), int(df_genres_base_filtered_global['release_year'].max())
        year_range_tab3 = st.slider(
            'Intervalo de Anos:', min_value=min_year_tab3, max_value=max_year_tab3,
            value=(min_year_tab3, max_year_tab3), key='tab3_years'
        )

    # Aplicar filtros (globais + específicos da aba)
    df_chart3_filtered = df_genres_base_filtered_global[
        df_genres_base_filtered_global['periodo'].isin(selected_periods_tab3) &
        (df_genres_base_filtered_global['release_year'] >= year_range_tab3[0]) &
        (df_genres_base_filtered_global['release_year'] <= year_range_tab3[1])
    ]

    # Criar o DataFrame agregado
    df_chart3 = df_chart3_filtered.groupby(['platform', 'genre']).size().reset_index(name='count')

    if not df_chart3.empty:
        fig3 = px.bar(
            df_chart3, x='count', y='genre', color='platform', facet_col='platform',
            facet_col_wrap=2, title='Gêneros Dominantes por Plataforma',
            labels={'count': 'Número de Jogos', 'genre': 'Gênero'},
            orientation='h', height=500
        )
        fig3.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Nenhum dado para exibir para o gráfico de Gêneros Dominantes com os filtros selecionados.")


# --- TAB 4: Top Desenvolvedores ---
with tab4:
    st.header("4. Top 10 Desenvolvedores por Lançamentos e Gênero")

    # Filtros específicos para esta aba (Período da Pandemia e Ano) + Top N
    st.subheader("Filtros Adicionais para esta Análise")
    col_filters_tab4_1, col_filters_tab4_2 = st.columns(2)
    with col_filters_tab4_1:
        all_periods_tab4 = ['Pré-Pandemia', 'Durante a Pandemia', 'Pós-Pandemia', 'Desconhecido']
        selected_periods_tab4 = st.multiselect(
            'Período(s) da Pandemia:', options=all_periods_tab4, default=all_periods_tab4, key='tab4_periods'
        )
    with col_filters_tab4_2:
        min_year_tab4, max_year_tab4 = int(df_genres_base_filtered_global['release_year'].min()), int(df_genres_base_filtered_global['release_year'].max())
        year_range_tab4 = st.slider(
            'Intervalo de Anos:', min_value=min_year_tab4, max_value=max_year_tab4,
            value=(min_year_tab4, max_year_tab4), key='tab4_years'
        )
    
    top_n_developers = st.slider(
        'Mostrar Top N Desenvolvedores:',
        min_value=5, max_value=25, value=10, step=1, key='top_n_devs'
    )

    # Aplicar filtros (globais + específicos da aba)
    df_filtered_tab4_temp = df_base_filtered_global[
        df_base_filtered_global['periodo'].isin(selected_periods_tab4) &
        (df_base_filtered_global['release_year'] >= year_range_tab4[0]) &
        (df_base_filtered_global['release_year'] <= year_range_tab4[1])
    ]

    df_genres_filtered_tab4_temp = df_genres_base_filtered_global[
        df_genres_base_filtered_global['periodo'].isin(selected_periods_tab4) &
        (df_genres_base_filtered_global['release_year'] >= year_range_tab4[0]) &
        (df_genres_base_filtered_global['release_year'] <= year_range_tab4[1])
    ]

    # Recalcular os top desenvolvedores com base nos dados filtrados (df_filtered_tab4_temp)
    developer_total_counts = df_filtered_tab4_temp.groupby('developers').size().reset_index(name='total_games')
    top_developers = developer_total_counts.sort_values('total_games', ascending=False).head(top_n_developers)['developers'].tolist()

    # Filtrar df_genres_filtered_tab4_temp pelos top_developers específicos
    df_chart4 = df_genres_filtered_tab4_temp[df_genres_filtered_tab4_temp['developers'].isin(top_developers)]
    df_chart4 = df_chart4.groupby(['developers', 'genre']).size().reset_index(name='count')

    if not df_chart4.empty:
        fig4 = px.bar(
            df_chart4, x='count', y='genre', color='genre', facet_col='developers',
            facet_col_wrap=3, title=f'Top {top_n_developers} Desenvolvedores por Lançamentos e Gênero',
            labels={'count': 'Número de Lançamentos', 'genre': 'Gênero', 'developers': 'Desenvolvedor'},
            orientation='h', height=600
        )
        fig4.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("Nenhum dado para exibir para o gráfico de Top Desenvolvedores com os filtros selecionados.")


# --- TAB 5: Preços por Gênero/Plataforma ---
with tab5:
    st.header("5. Distribuição de Preços (Dólar) por Plataforma e Gênero")

    # Filtros específicos para esta aba (Período da Pandemia e Ano)
    st.subheader("Filtros Adicionais para esta Análise")
    col_filters_tab5_1, col_filters_tab5_2 = st.columns(2)
    with col_filters_tab5_1:
        all_periods_tab5 = ['Pré-Pandemia', 'Durante a Pandemia', 'Pós-Pandemia', 'Desconhecido']
        selected_periods_tab5 = st.multiselect(
            'Período(s) da Pandemia:', options=all_periods_tab5, default=all_periods_tab5, key='tab5_periods'
        )
    with col_filters_tab5_2:
        min_year_tab5, max_year_tab5 = int(df_genres_base_filtered_global['release_year'].min()), int(df_genres_base_filtered_global['release_year'].max())
        year_range_tab5 = st.slider(
            'Intervalo de Anos:', min_value=min_year_tab5, max_value=max_year_tab5,
            value=(min_year_tab5, max_year_tab5), key='tab5_years'
        )

    # Aplicar filtros (globais + específicos da aba)
    df_chart5 = df_genres_base_filtered_global[
        df_genres_base_filtered_global['periodo'].isin(selected_periods_tab5) &
        (df_genres_base_filtered_global['release_year'] >= year_range_tab5[0]) &
        (df_genres_base_filtered_global['release_year'] <= year_range_tab5[1])
    ][['platform', 'genre', 'preco_dolar']]

    if not df_chart5.empty:
        fig5 = px.box(
            df_chart5, x='platform', y='preco_dolar', color='genre',
            title='Distribuição de Preços (Dólar) por Plataforma e Gênero',
            labels={'platform': 'Plataforma', 'preco_dolar': 'Preço em Dólar', 'genre': 'Gênero'},
            log_y=True, height=500
        )
        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.info("Nenhum dado para exibir para o gráfico de Preços com os filtros selecionados.")


# --- TAB 6: Visão Hierárquica (4 Sunbursts) ---
with tab6:
    st.header("6. Distribuição Hierárquica de Lançamentos (Plataforma -> Gênero)")
    st.markdown("Analise a distribuição de jogos por Plataforma e Gênero para diferentes períodos.")

    col_s1, col_s2 = st.columns(2) # Duas colunas para Sunbursts

    # Sunburst 1: Período Completo
    with col_s1:
        st.subheader("Período Completo")
        # df_chart6_complete usa df_genres_base_filtered_global diretamente
        if not df_genres_base_filtered_global.empty:
            fig_complete = px.sunburst(
                df_genres_base_filtered_global,
                path=['platform', 'genre'], # Hierarquia: Plataforma -> Gênero
                values='gameid', # Conta o número de gameids
                color='platform', # Colore a fatia principal pela plataforma
                title='Período Completo',
                height=500 # Altura para melhor visualização
            )
            fig_complete.update_traces(hovertemplate='<b>%{label}</b><br>Contagem: %{value}<extra></extra>')
            st.plotly_chart(fig_complete, use_container_width=True)
        else:
            st.info("Nenhum dado para o Sunburst do Período Completo.")

    # Sunburst 2: Pré-Pandemia
    with col_s2:
        st.subheader("Pré-Pandemia")
        df_pre_pandemic_sunburst = df_genres_base_filtered_global[
            df_genres_base_filtered_global['periodo'] == 'Pré-Pandemia'
        ]
        if not df_pre_pandemic_sunburst.empty:
            fig_pre_pandemic = px.sunburst(
                df_pre_pandemic_sunburst,
                path=['platform', 'genre'],
                values='gameid',
                color='platform',
                title='Pré-Pandemia',
                height=500
            )
            fig_pre_pandemic.update_traces(hovertemplate='<b>%{label}</b><br>Contagem: %{value}<extra></extra>')
            st.plotly_chart(fig_pre_pandemic, use_container_width=True)
        else:
            st.info("Nenhum dado para o Sunburst da Pré-Pandemia.")

    st.divider() # Adiciona uma linha divisória com espaço

    col_s3, col_s4 = st.columns(2) # Mais duas colunas para os Sunbursts restantes

    # Sunburst 3: Durante a Pandemia
    with col_s3:
        st.subheader("Durante a Pandemia")
        df_during_pandemic_sunburst = df_genres_base_filtered_global[
            df_genres_base_filtered_global['periodo'] == 'Durante a Pandemia'
        ]
        if not df_during_pandemic_sunburst.empty:
            fig_during_pandemic = px.sunburst(
                df_during_pandemic_sunburst,
                path=['platform', 'genre'],
                values='gameid',
                color='platform',
                title='Durante a Pandemia',
                height=500
            )
            fig_during_pandemic.update_traces(hovertemplate='<b>%{label}</b><br>Contagem: %{value}<extra></extra>')
            st.plotly_chart(fig_during_pandemic, use_container_width=True)
        else:
            st.info("Nenhum dado para o Sunburst Durante a Pandemia.")

    # Sunburst 4: Pós-Pandemia
    with col_s4:
        st.subheader("Pós-Pandemia")
        df_post_pandemic_sunburst = df_genres_base_filtered_global[
            df_genres_base_filtered_global['periodo'] == 'Pós-Pandemia'
        ]
        if not df_post_pandemic_sunburst.empty:
            fig_post_pandemic = px.sunburst(
                df_post_pandemic_sunburst,
                path=['platform', 'genre'],
                values='gameid',
                color='platform',
                title='Pós-Pandemia',
                height=500
            )
            fig_post_pandemic.update_traces(hovertemplate='<b>%{label}</b><br>Contagem: %{value}<extra></extra>')
            st.plotly_chart(fig_post_pandemic, use_container_width=True)
        else:
            st.info("Nenhum dado para o Sunburst Pós-Pandemia.")


st.sidebar.header("Informações do Dashboard")
st.sidebar.info(
    "Este dashboard interativo permite explorar dados de jogos com filtros globais (Plataforma e Gênero). "
    "Mude as abas para ver diferentes análises. "
    "Dentro de cada aba, você encontrará filtros adicionais (Período da Pandemia, Intervalo de Anos, etc.) que são específicos para aquela análise."
)