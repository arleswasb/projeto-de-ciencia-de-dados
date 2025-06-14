import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Configuração da página Streamlit ---
st.set_page_config(layout="wide", page_title="Dashboard de Análise de Jogos")

st.title("🎮 Dashboard de Análise de Jogos")
st.markdown("Explore dados sobre lançamentos, gêneros, desenvolvedores e preços de jogos.")

# Define year ranges for pandemic periods globally
period_ranges = {
    'Pré-Pandemia': (1998, 2019),
    'Pandemia': (2020, 2021),
    'Pós-Pandemia': (2022, 2025)
}

# --- Carregar e Preparar os Dados (Diretamente no Streamlit) ---
@st.cache_data # Decorador para cachear os dados e evitar recarregamento a cada interação
def load_and_preprocess_data():
    """Carrega o dataset e realiza todas as etapas de pré-processamento."""
    try:
        df = pd.read_csv('DB_completo.csv')
    except FileNotFoundError:
        st.error("ERRO: DB_completo.csv não encontrado. Por favor, certifique-se de que o arquivo está na mesma pasta do script.")
        st.stop()

    df.drop_duplicates(inplace=True)

    genre_columns = [col for col in df.columns if col.startswith('genre_')]
    df['genre'] = df.apply(
        lambda row: [col.replace('genre_', '') for col in genre_columns if row[col]],
        axis=1
    )
    df['genre'] = df['genre'].apply(lambda x: x[0] if x else 'Outros')

    df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
    df.dropna(subset=['release_year'], inplace=True)
    df['release_year'] = df['release_year'].astype(int)

    df['preco_dolar'] = pd.to_numeric(df['preco_dolar'], errors='coerce')
    df.dropna(subset=['preco_dolar'], inplace=True)

    df['developers'] = df['developers'].fillna('Desconhecido') # Corrigido: 'developer' para 'developers'
    df['platform'] = df['platform'].fillna('Outra')

    return df

df_processed = load_and_preprocess_data()

# --- Filtros Globais na Barra Lateral ---
all_platforms = ['Todas'] + sorted(df_processed['platform'].unique().tolist())
selected_platform = st.sidebar.selectbox("Filtrar por Plataforma:", all_platforms, key='global_platform')

all_genres = ['Todos'] + sorted(df_processed['genre'].unique().tolist())
selected_genre = st.sidebar.selectbox("Filtrar por Gênero:", all_genres, key='global_genre')

df_global_filtered = df_processed.copy()
if selected_platform != 'Todas':
    df_global_filtered = df_global_filtered[df_global_filtered['platform'] == selected_platform]
if selected_genre != 'Todos':
    df_global_filtered = df_global_filtered[df_global_filtered['genre'] == selected_genre]

# Helper function to apply pandemic period and year range filters
def get_tab_filtered_data_and_year_slider(df_base, tab_key_suffix):
    """
    Aplica filtros de período da pandemia e intervalo de anos, e cria o slider de anos.
    Retorna o DataFrame final filtrado para a aba.
    """
    # Período da Pandemia filter (now without "Período Completo")
    selected_pandemic_periods = st.sidebar.multiselect(
        f"Período da Pandemia (Tab {tab_key_suffix}):",
        options=['Pré-Pandemia', 'Pandemia', 'Pós-Pandemia'],
        default=['Pré-Pandemia', 'Pandemia', 'Pós-Pandemia'], # Default to all
        key=f'pandemic_periods_{tab_key_suffix}'
    )

    df_filtered_by_pandemic = pd.DataFrame()
    if selected_pandemic_periods:
        for period in selected_pandemic_periods:
            min_p, max_p = period_ranges.get(period, (None, None))
            if min_p is not None and max_p is not None:
                df_filtered_by_pandemic = pd.concat([df_filtered_by_pandemic,
                                                       df_base[
                                                           (df_base['release_year'] >= min_p) &
                                                           (df_base['release_year'] <= max_p)
                                                       ]])
        df_filtered_by_pandemic.drop_duplicates(inplace=True)
    else:
        # If no pandemic period is selected, display a warning and ensure df_filtered_by_pandemic is empty
        st.info(f"Selecione pelo menos um 'Período da Pandemia' para filtrar os dados na Tab {tab_key_suffix}.")
        # No need to set df_filtered_by_pandemic = pd.DataFrame() here, as it's initialized as such.
        # The subsequent checks for .empty will handle chart rendering.

    # Determine dynamic min/max for the year slider
    if not df_filtered_by_pandemic.empty:
        dynamic_min_year = int(df_filtered_by_pandemic['release_year'].min())
        dynamic_max_year = int(df_filtered_by_pandemic['release_year'].max())
    else:
        # Fallback for slider range: use the base dataframe's full range of the original df_processed
        # This ensures the slider always has a range even if no pandemic periods are selected,
        # but the charts will be empty due to df_filtered_by_pandemic being empty.
        dynamic_min_year = int(df_processed['release_year'].min())
        dynamic_max_year = int(df_processed['release_year'].max())


    # Ensure the default value for the slider respects the dynamic range
    # Get current state if it exists, otherwise set to full dynamic range
    current_slider_value = st.session_state.get(f'years_{tab_key_suffix}', (dynamic_min_year, dynamic_max_year))

    # Adjust current_slider_value if it goes out of bounds of the new dynamic range
    adjusted_min_val = max(dynamic_min_year, current_slider_value[0])
    adjusted_max_val = min(dynamic_max_year, current_slider_value[1])

    # If the adjusted range is invalid (min somehow becomes greater than max due to aggressive filtering),
    # reset to the full dynamic range.
    if adjusted_min_val > adjusted_max_val:
        adjusted_min_val = dynamic_min_year
        adjusted_max_val = dynamic_max_year
    
    initial_slider_value = (adjusted_min_val, adjusted_max_val)


    selected_years_tuple = st.sidebar.slider(
        f'Intervalo de Anos (Tab {tab_key_suffix})',
        min_value=dynamic_min_year,
        max_value=dynamic_max_year,
        value=initial_slider_value,
        key=f'years_{tab_key_suffix}'
    )

    # Final filter with the year range
    if not df_filtered_by_pandemic.empty:
        df_final_filtered = df_filtered_by_pandemic[
            (df_filtered_by_pandemic['release_year'] >= selected_years_tuple[0]) &
            (df_filtered_by_pandemic['release_year'] <= selected_years_tuple[1])
        ]
    else:
        df_final_filtered = pd.DataFrame() # Returns empty if pandemic period filter resulted in empty df

    return df_final_filtered


# --- Tabs ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Visão Geral de Lançamentos e Gêneros",
    "Análise por Plataforma e Desenvolvedor",
    "Distribuição de Preços",
    "Tendências de Lançamento por Período",
    "Visão Hierárquica por Gênero e Período"
])

# --- Tab 1: Visão Geral de Lançamentos e Gêneros ---
with tab1:
    st.header("Visão Geral de Lançamentos e Gêneros")
    df_tab1 = get_tab_filtered_data_and_year_slider(df_global_filtered, '1')

    if not df_tab1.empty:
        # Gráfico 1: Jogos Lançados por Ano (Gráfico de Barras)
        st.subheader("1. Jogos Lançados por Ano")
        df_jogos_por_ano = df_tab1.groupby('release_year').size().reset_index(name='count')
        if not df_jogos_por_ano.empty:
            fig1 = px.bar(df_jogos_por_ano, x='release_year', y='count', title='Jogos Lançados por Ano')
            fig1.update_xaxes(dtick=1, tickformat="%Y")
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("Nenhum dado de jogos lançados por ano com os filtros selecionados.")

        # Gráfico 2: Top 10 Gêneros por Número de Lançamentos (Gráfico de Barras)
        st.subheader("2. Top 10 Gêneros por Número de Lançamentos")
        df_generos_count = df_tab1['genre'].value_counts().nlargest(10).reset_index()
        df_generos_count.columns = ['genre', 'count']
        if not df_generos_count.empty:
            fig2 = px.bar(df_generos_count, x='genre', y='count',
                        title='Top 10 Gêneros por Número de Lançamentos')
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Nenhum dado de top 10 gêneros com os filtros selecionados.")

        # Gráfico 3: Distribuição de Preços por Gênero (Box Plot ou Histograma)
        st.subheader("3. Distribuição de Preços por Gênero")
        if not df_tab1.empty:
            # Vamos limitar os gêneros a serem exibidos para evitar um gráfico muito poluído
            top_genres = df_tab1['genre'].value_counts().nlargest(10).index
            df_price_genre = df_tab1[df_tab1['genre'].isin(top_genres)]

            if not df_price_genre.empty:
                fig3 = px.box(df_price_genre, x='genre', y='preco_dolar',
                            title='Distribuição de Preços (Dólar) por Gênero (Top 10)',
                            labels={'preco_dolar': 'Preço (Dólar)'},
                            height=500)
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.info("Nenhum dado de distribuição de preços por gênero com os filtros selecionados.")
        else:
            st.info("Nenhum dado de distribuição de preços por gênero com os filtros selecionados.")

    else:
        st.info("Nenhum dado para exibir na Visão Geral de Lançamentos e Gêneros com os filtros globais ou de período da pandemia selecionados.")

# --- Tab 2: Análise por Plataforma e Desenvolvedor ---
with tab2:
    st.header("Análise por Plataforma e Desenvolvedor")
    df_tab2 = get_tab_filtered_data_and_year_slider(df_global_filtered, '2')

    if not df_tab2.empty:
        # Gráfico 4: Lançamentos por Plataforma ao Longo do Tempo (Gráfico de Linha)
        st.subheader("4. Lançamentos por Plataforma ao Longo do Tempo")
        df_platform_releases_over_time = df_tab2.groupby(['release_year', 'platform']).size().reset_index(name='count')
        if not df_platform_releases_over_time.empty:
            fig4 = px.line(df_platform_releases_over_time, x='release_year', y='count', color='platform',
                        title='Lançamentos por Plataforma ao Longo do Tempo',
                        labels={'release_year': 'Ano de Lançamento', 'count': 'Número de Lançamentos'})
            fig4.update_xaxes(dtick=1, tickformat="%Y")
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("Nenhum dado de lançamentos por plataforma ao longo do tempo com os filtros selecionados.")

        # Gráfico 5: Top 10 Desenvolvedores por Número de Lançamentos
        st.subheader("5. Top 10 Desenvolvedores por Número de Lançamentos")
        # Slider para selecionar o número de desenvolvedores a mostrar
        top_n_devs = st.slider("Mostrar Top N Desenvolvedores:", 5, 20, 10, key='top_devs_tab2')

        df_dev_count = df_tab2['developers'].value_counts().nlargest(top_n_devs).reset_index() # CORRIGIDO AQUI
        df_dev_count.columns = ['developers', 'count'] # CORRIGIDO AQUI
        if not df_dev_count.empty:
            fig5 = px.bar(df_dev_count, x='developers', y='count', # CORRIGIDO AQUI
                        title=f'Top {top_n_devs} Desenvolvedores por Número de Lançamentos')
            st.plotly_chart(fig5, use_container_width=True)
        else:
            st.info("Nenhum dado de top desenvolvedores com os filtros selecionados.")

        # Gráfico 6: Distribuição de Preços por Plataforma (Box Plot)
        st.subheader("6. Distribuição de Preços por Plataforma")
        if not df_tab2.empty:
            # Filtra para as plataformas mais relevantes ou todas
            top_platforms = df_tab2['platform'].value_counts().nlargest(10).index
            df_price_platform = df_tab2[df_tab2['platform'].isin(top_platforms)]

            if not df_price_platform.empty:
                fig6 = px.box(df_price_platform, x='platform', y='preco_dolar',
                            title='Distribuição de Preços (Dólar) por Plataforma (Top 10)',
                            labels={'preco_dolar': 'Preço (Dólar)'},
                            height=500)
                st.plotly_chart(fig6, use_container_width=True)
            else:
                st.info("Nenhum dado de distribuição de preços por plataforma com os filtros selecionados.")
        else:
            st.info("Nenhum dado de distribuição de preços por plataforma com os filtros selecionados.")

    else:
        st.info("Nenhum dado para exibir na Análise por Plataforma e Desenvolvedor com os filtros globais ou de período da pandemia selecionados.")

# --- Tab 3: Distribuição de Preços ---
with tab3:
    st.header("Distribuição de Preços")
    df_tab3 = get_tab_filtered_data_and_year_slider(df_global_filtered, '3')

    if not df_tab3.empty:
        # Gráfico 7: Histograma Geral de Preços em Dólar
        st.subheader("7. Histograma Geral de Preços em Dólar")
        if not df_tab3.empty:
            fig7 = px.histogram(df_tab3, x='preco_dolar', nbins=50,
                                title='Distribuição de Preços em Dólar',
                                labels={'preco_dolar': 'Preço (Dólar)'})
            st.plotly_chart(fig7, use_container_width=True)
        else:
            st.info("Nenhum dado de histograma geral de preços com os filtros selecionados.")

        # Gráfico 8: Tendência de Preços Médios ao Longo do Tempo (por Plataforma ou Gênero)
        st.subheader("8. Tendência de Preços Médios ao Longo do Tempo")
        trend_by_option_tab8 = st.selectbox(
            "Analisar tendência de preço por:",
            ('Plataforma', 'Gênero'),
            key='trend_option_tab8'
        )

        df_chart8_filtered = df_tab3 # Já vem filtrado pela função get_tab_filtered_data_and_year_slider

        if not df_chart8_filtered.empty:
            if trend_by_option_tab8 == 'Plataforma':
                df_line_chart_data = df_chart8_filtered.groupby(['release_year', 'platform'])['preco_dolar'].mean().reset_index()
                color_by_line = 'platform'
                title_suffix_line = 'por Plataforma'
            else: # trend_by_option_tab8 == 'Gênero'
                df_line_chart_data = df_chart8_filtered.groupby(['release_year', 'genre'])['preco_dolar'].mean().reset_index()
                color_by_line = 'genre'
                title_suffix_line = 'por Gênero'

            if not df_line_chart_data.empty:
                fig8 = px.line(
                    df_line_chart_data,
                    x='release_year',
                    y='preco_dolar',
                    color=color_by_line,
                    title=f'Tendência de Preços Médios {title_suffix_line}',
                    labels={'release_year': 'Ano de Lançamento', 'preco_dolar': 'Preço Médio (Dólar)'},
                    height=500
                )
                fig8.update_xaxes(dtick=1, tickformat="%Y", showgrid=True) 
                st.plotly_chart(fig8, use_container_width=True)
            else:
                st.info("Nenhum dado para exibir para a Tendência de Preços com os filtros selecionados.")
        else:
            st.info("Nenhum dado para exibir para a Tendência de Preços com os filtros selecionados.")
    else:
        st.info("Nenhum dado para exibir na Distribuição de Preços com os filtros globais ou de período da pandemia selecionados.")

# --- Tab 4: Tendências de Lançamento por Período ---
with tab4:
    st.header("Tendências de Lançamento por Período")
    df_tab4 = get_tab_filtered_data_and_year_slider(df_global_filtered, '4')

    if not df_tab4.empty:
        # Gráfico 9: Lançamentos Anuais por Gênero (Gráfico de Barras Empilhadas)
        st.subheader("9. Lançamentos Anuais por Gênero")
        df_genre_releases_annual = df_tab4.groupby(['release_year', 'genre']).size().reset_index(name='count')
        if not df_genre_releases_annual.empty:
            fig9 = px.bar(df_genre_releases_annual, x='release_year', y='count', color='genre',
                        title='Lançamentos Anuais por Gênero',
                        labels={'release_year': 'Ano de Lançamento', 'count': 'Número de Lançamentos'},
                        hover_name='genre')
            fig9.update_xaxes(dtick=1, tickformat="%Y")
            st.plotly_chart(fig9, use_container_width=True)
        else:
            st.info("Nenhum dado de lançamentos anuais por gênero com os filtros selecionados.")

        # Gráfico 10: Top 5 Gêneros por Período de Lançamento (Comparativo)
        st.subheader("10. Top 5 Gêneros por Período de Lançamento (Comparativo)")
        # Criar a coluna de período com base nos ranges
        def get_period_label(year):
            if 1998 <= year <= 2019:
                return 'Pré-Pandemia'
            elif 2020 <= year <= 2021:
                return 'Pandemia'
            elif 2022 <= year <= 2025:
                return 'Pós-Pandemia'
            return 'Outro'

        df_tab4_with_period = df_tab4.copy()
        df_tab4_with_period['period_label'] = df_tab4_with_period['release_year'].apply(get_period_label)

        # Contar lançamentos por gênero e período, e pegar o top 5 por período
        df_genre_period = df_tab4_with_period.groupby(['period_label', 'genre']).size().reset_index(name='count')
        
        # Filtro para incluir apenas os períodos que estão presentes no df_tab4_with_period
        # e que foram selecionados no multiselect
        selected_pandemic_periods_tab4_from_state = st.session_state.get('pandemic_periods_4', ['Pré-Pandemia', 'Pandemia', 'Pós-Pandemia'])
        df_genre_period = df_genre_period[df_genre_period['period_label'].isin(selected_pandemic_periods_tab4_from_state)]


        if not df_genre_period.empty:
            # Função para obter top N gêneros por grupo
            def get_top_n(df_group, n=5):
                return df_group.nlargest(n, 'count')

            # Aplicar a função para cada período
            top_genres_by_period = df_genre_period.groupby('period_label', group_keys=False).apply(get_top_n)

            if not top_genres_by_period.empty:
                fig10 = px.bar(top_genres_by_period, x='genre', y='count', color='period_label',
                            barmode='group',
                            title='Top Gêneros por Período de Lançamento',
                            labels={'genre': 'Gênero', 'count': 'Número de Lançamentos', 'period_label': 'Período'},
                            height=500)
                st.plotly_chart(fig10, use_container_width=True)
            else:
                st.info("Nenhum dado de top gêneros por período para exibir com os filtros selecionados.")
        else:
            st.info("Nenhum dado de top gêneros por período para exibir com os filtros selecionados.")
    else:
        st.info("Nenhum dado para exibir nas Tendências de Lançamento por Período com os filtros globais ou de período da pandemia selecionados.")


# --- Tab 5: Visão Hierárquica por Gênero e Período ---
with tab5:
    st.header("Visão Hierárquica por Gênero e Período")
    df_tab5 = get_tab_filtered_data_and_year_slider(df_global_filtered, '5')

    if not df_tab5.empty:
        # Gráficos Sunburst para explorar a hierarquia de Gênero, Plataforma, Desenvolvedor, e Preço Médio.
        # Gráfico Sunburst para Gênero -> Plataforma -> Número de Lançamentos
        st.subheader("11. Gênero -> Plataforma (Número de Lançamentos)")
        df_sunburst1 = df_tab5.groupby(['genre', 'platform']).size().reset_index(name='count')
        if not df_sunburst1.empty:
            fig11 = px.sunburst(df_sunburst1, path=['genre', 'platform'], values='count',
                                title='Distribuição de Lançamentos por Gênero e Plataforma')
            st.plotly_chart(fig11, use_container_width=True)
        else:
            st.info("Nenhum dado para o Sunburst Gênero -> Plataforma com os filtros selecionados.")

        # Gráfico Sunburst para Período -> Gênero -> Número de Lançamentos
        st.subheader("12. Período -> Gênero (Número de Lançamentos)")
        def get_period_label_for_sunburst(year):
            if 1998 <= year <= 2019: return 'Pré-Pandemia'
            elif 2020 <= year <= 2021: return 'Pandemia'
            elif 2022 <= year <= 2025: return 'Pós-Pandemia'
            return 'Outro'

        df_sunburst2 = df_tab5.copy()
        df_sunburst2['period_label'] = df_sunburst2['release_year'].apply(get_period_label_for_sunburst)
        
        # Filtrar apenas os períodos que foram selecionados para esta tab
        # Pega a lista de períodos selecionados para a Tab 5 do st.session_state
        selected_pandemic_periods_tab5_from_state = st.session_state.get('pandemic_periods_5', ['Pré-Pandemia', 'Pandemia', 'Pós-Pandemia'])
        df_sunburst2 = df_sunburst2[df_sunburst2['period_label'].isin(selected_pandemic_periods_tab5_from_state)]


        df_sunburst2_agg = df_sunburst2.groupby(['period_label', 'genre']).size().reset_index(name='count')
        if not df_sunburst2_agg.empty:
            fig12 = px.sunburst(df_sunburst2_agg, path=['period_label', 'genre'], values='count',
                                title='Distribuição de Lançamentos por Período e Gênero')
            st.plotly_chart(fig12, use_container_width=True)
        else:
            st.info("Nenhum dado para o Sunburst Período -> Gênero com os filtros selecionados.")

        # Gráfico Sunburst para Desenvolvedor -> Gênero -> Número de Lançamentos
        st.subheader("13. Desenvolvedor -> Gênero (Número de Lançamentos)")
        df_sunburst3 = df_tab5.groupby(['developers', 'genre']).size().reset_index(name='count') # CORRIGIDO AQUI
        # Pode ser interessante limitar o número de desenvolvedores ou gêneros para não poluir demais
        # Por simplicidade, vamos usar todos os desenvolvedores filtrados aqui
        if not df_sunburst3.empty:
            fig13 = px.sunburst(df_sunburst3, path=['developers', 'genre'], values='count', # CORRIGIDO AQUI
                                title='Distribuição de Lançamentos por Desenvolvedor e Gênero')
            st.plotly_chart(fig13, use_container_width=True)
        else:
            st.info("Nenhum dado para o Sunburst Desenvolvedor -> Gênero com os filtros selecionados.")

        # Gráfico Sunburst para Gênero -> Preço Médio
        st.subheader("14. Gênero -> Preço Médio (Total)")
        # Para Sunburst com agregação de métricas, precisa de um campo de 'parent' e 'labels' e 'values'
        # Aqui, vamos usar a soma dos preços por gênero como exemplo de valor.
        df_sunburst4 = df_tab5.groupby('genre')['preco_dolar'].sum().reset_index()
        if not df_sunburst4.empty:
            fig14 = px.sunburst(df_sunburst4, path=['genre'], values='preco_dolar',
                                title='Total de Preços (Dólar) por Gênero')
            st.plotly_chart(fig14, use_container_width=True)
        else:
            st.info("Nenhum dado para o Sunburst Gênero -> Preço Médio com os filtros selecionados.")

    else:
        st.info("Nenhum dado para exibir na Visão Hierárquica por Gênero e Período com os filtros globais ou de período da pandemia selecionados.")

st.sidebar.markdown("---")
st.sidebar.info(
    "Este dashboard interativo permite explorar dados de jogos, incluindo tendências de lançamento, "
    "preferências de gênero, atividades de desenvolvedores e distribuição de preços."
)