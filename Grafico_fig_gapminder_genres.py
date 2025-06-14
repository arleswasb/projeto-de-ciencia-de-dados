import pandas as pd
import plotly.express as px
import os

# --- 1. Carregamento do DataFrame ---
caminho_arquivo = os.path.join(r"E:\UFRN 2025_1\CIENCIA DE DADOS\tarefa1\trabalhoP2\DB_completo_plataformas.csv")
df = pd.read_csv(caminho_arquivo)

print("DataFrame carregado com sucesso.")
print(df.head())
print(df.info())
print("-" * 50)

# --- Preparação dos dados para o gráfico Gapminder ---
print("\nGerando gráfico: Análise de Gêneros (Estilo Gapminder)")
try:
    # 1. Derreter as colunas de gênero
    df_genres_melted = df.melt(
        id_vars=['release_year', 'preco_dolar'],
        value_vars=[col for col in df.columns if col.startswith('genre_')],
        var_name='genre_full',
        value_name='is_genre'
    )

    # 2. Filtrar apenas os registros onde o gênero é True
    df_genres_gapminder = df_genres_melted[df_genres_melted['is_genre'] == True].copy()

    # 3. Extrair o nome do gênero
    df_genres_gapminder['genre'] = df_genres_gapminder['genre_full'].str.replace('genre_', '')

    # 4. Obter todos os gêneros únicos e anos únicos
    all_genres = df_genres_gapminder['genre'].unique()
    all_years = sorted(df['release_year'].unique())

    # 5. Criar todas as combinações possíveis de ano e gênero
    index_df = pd.MultiIndex.from_product([all_years, all_genres], names=['release_year', 'genre']).to_frame(index=False)

    # 6. Agrupar e contar os jogos por ano e gênero
    genre_yearly_counts = df_genres_gapminder.groupby(['release_year', 'genre']).agg(
        game_count=('genre', 'count'),
        avg_price=('preco_dolar', 'mean')
    ).reset_index()

    # 7. Fazer um LEFT JOIN com todas as combinações e preencher NaN com 0
    genre_yearly_stats = pd.merge(index_df, genre_yearly_counts, on=['release_year', 'genre'], how='left').fillna(0)

    # 8. Converter 'release_year' para string para usar na animação
    genre_yearly_stats['release_year_str'] = genre_yearly_stats['release_year'].astype(str)

    # Criar o gráfico Gapminder
    fig_gapminder_genres = px.scatter(
        genre_yearly_stats,
        x='avg_price',
        y='game_count',
        size='game_count',
        color='genre',
        hover_name='genre',
        animation_frame='release_year_str',  # Usar a coluna de string aqui
        animation_group='genre',
        log_x=False,
        size_max=60,
        range_x=[genre_yearly_stats['avg_price'].min() * 0.8 if not genre_yearly_stats['avg_price'].empty else 0,
                 genre_yearly_stats['avg_price'].max() * 1.2 if not genre_yearly_stats['avg_price'].empty else 1],
        range_y=[0, genre_yearly_stats['game_count'].max() * 1.2 if not genre_yearly_stats['game_count'].empty else 1],
        title='Análise de Gêneros ao Longo dos Anos (Estilo Gapminder)',
        labels={
            'avg_price': 'Preço Médio (Dólar)',
            'game_count': 'Número de Jogos Lançados',
            'release_year_str': 'Ano de Lançamento',  # Atualizar o rótulo
            'genre': 'Gênero'
        },
        category_orders={'release_year_str': [str(year) for year in all_years]}  # Definir a ordem da animação
    )

    # Ajustar a velocidade da animação (opcional)
    fig_gapminder_genres.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 500
    fig_gapminder_genres.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 300

    fig_gapminder_genres.show()
    fig_gapminder_genres.write_html("gapminder_genres.html")

except KeyError as e:
    print(f"Erro: Coluna não encontrada para o gráfico Gapminder: {e}. Verifique 'release_year', 'preco_dolar', e as colunas 'genre_'.")
except Exception as e:
    print(f"Erro ao gerar o gráfico Gapminder para análise de gêneros: {e}")