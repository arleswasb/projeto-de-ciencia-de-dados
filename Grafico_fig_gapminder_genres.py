import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import calendar
import numpy as np
import os

# --- 1. Criação de um DataFrame de exemplo (simulando a estrutura fornecida) ---
# Em um cenário real, você carregaria seu DataFrame aqui (ex: pd.read_csv('seu_arquivo.csv'))


caminho_arquivo = os.path.join(r"E:\UFRN 2025_1\CIENCIA DE DADOS\tarefa1\trabalhoP2\DB_completo_plataformas.csv")
data = pd.read_csv(caminho_arquivo)


df = pd.DataFrame(data)

print("DataFrame de exemplo criado com sucesso. Primeiras 5 linhas:")
print(df.head())
print("\nInformações do DataFrame:")
df.info()
print("-" * 50)


# --- 5. Gráfico Gapminder para Análise de Gêneros ---
print("\nGerando gráfico: Análise de Gêneros (Estilo Gapminder)")

# Preparar os dados para o gráfico Gapminder
# 1. Derreter as colunas de gênero para formato longo
df_genres_gapminder = df.melt(
    id_vars=['release_year', 'preco_dolar'],
    value_vars=genre_columns,
    var_name='genre_full',
    value_name='is_genre'
)

# 2. Filtrar apenas os registros onde o gênero é verdadeiro
df_genres_gapminder = df_genres_gapminder[df_genres_gapminder['is_genre'] == True]

# 3. Remover o prefixo 'genre_' do nome do gênero
df_genres_gapminder['genre'] = df_genres_gapminder['genre_full'].str.replace('genre_', '')

# 4. Agrupar por ano e gênero para calcular o preço médio e a contagem de jogos
genre_yearly_stats = df_genres_gapminder.groupby(['release_year', 'genre']).agg(
    avg_price=('preco_dolar', 'mean'),
    game_count=('genre', 'count')
).reset_index()

# Criar o gráfico Gapminder
fig_gapminder_genres = px.scatter(
    genre_yearly_stats,
    x='avg_price',
    y='game_count',
    size='game_count', # O tamanho da bolha reflete o número de jogos
    color='genre',     # A cor da bolha é o gênero
    hover_name='genre', # Nome do gênero ao passar o mouse
    animation_frame='release_year', # Animação ao longo dos anos
    animation_group='genre', # Garante que as bolhas do mesmo gênero se movem suavemente
    log_x=False, # Não usar escala logarítmica para o preço, a menos que seja necessário
    size_max=60, # Tamanho máximo das bolhas
    range_x=[genre_yearly_stats['avg_price'].min() * 0.8, genre_yearly_stats['avg_price'].max() * 1.2],
    range_y=[0, genre_yearly_stats['game_count'].max() * 1.2],
    title='Análise de Gêneros ao Longo dos Anos (Estilo Gapminder)',
    labels={
        'avg_price': 'Preço Médio (Dólar)',
        'game_count': 'Número de Jogos Lançados',
        'release_year': 'Ano de Lançamento'
    }
)

# Ajustar a velocidade da animação (opcional)
fig_gapminder_genres.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 500
fig_gapminder_genres.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 300

fig_gapminder_genres.show()
fig_gapminder_genres.write_html("gapminder_genres.html") # Salva o gráfico como HTML

