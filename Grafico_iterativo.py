import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import calendar
import numpy as np

# --- 1. Criação de um DataFrame de exemplo (simulando a estrutura fornecida) ---
# Em um cenário real, você carregaria seu DataFrame aqui (ex: pd.read_csv('seu_arquivo.csv'))

# Gerando dados fictícios para demonstração
np.random.seed(42) # Para reprodutibilidade

num_games = 1000 # Reduzido para melhor visualização em exemplos
data = {
    'gameid': range(1, num_games + 1),
    'title': [f'Game Title {i}' for i in range(num_games)],
    'platform': np.random.choice(['PC', 'PlayStation', 'Xbox', 'Nintendo Switch', 'Mobile'], num_games),
    'developers': np.random.choice([f'Dev Studio {i}' for i in range(20)], num_games),
    'publishers': np.random.choice([f'Publisher Co. {i}' for i in range(15)], num_games),
    'release_month': np.random.randint(1, 13, num_games),
    'release_year': np.random.randint(2000, 2024, num_games),
    'genre_Aventura': np.random.choice([True, False], num_games, p=[0.6, 0.4]),
    'genre_Ação': np.random.choice([True, False], num_games, p=[0.7, 0.3]),
    'genre_Competição Online': np.random.choice([True, False], num_games, p=[0.2, 0.8]),
    'genre_Esportes': np.random.choice([True, False], num_games, p=[0.15, 0.85]),
    'genre_Outros': np.random.choice([True, False], num_games, p=[0.3, 0.7]),
    'genre_RPG': np.random.choice([True, False], num_games, p=[0.4, 0.6]),
    'genre_Simulação': np.random.choice([True, False], num_games, p=[0.25, 0.75]),
    'preco_dolar': np.random.uniform(5.0, 70.0, num_games).round(2),
    'preco_euro': np.random.uniform(4.0, 65.0, num_games).round(2)
}
df = pd.DataFrame(data)

print("DataFrame de exemplo criado com sucesso. Primeiras 5 linhas:")
print(df.head())
print("\nInformações do DataFrame:")
df.info()
print("-" * 50)

# --- 2. Análise Univariada ---

# 2.1. Distribuição de Jogos por Plataforma
# Um gráfico de barras é ideal para visualizar a contagem de cada categoria.
print("\nGerando gráfico: Contagem de Jogos por Plataforma")
platform_counts = df['platform'].value_counts().reset_index()
platform_counts.columns = ['platform_name', 'count'] # Renomeando as colunas para evitar conflitos com 'index' ou nome da coluna original

fig_platform_count = px.bar(
    platform_counts,
    x='platform_name',
    y='count',
    title='Contagem de Jogos por Plataforma',
    labels={'platform_name': 'Plataforma', 'count': 'Número de Jogos'},
    color='platform_name' # Colore as barras pela plataforma
)
fig_platform_count.show()
fig_platform_count.write_html("platform_count.html") # Salva o gráfico como HTML

# 2.2. Distribuição de Lançamentos por Ano
# Um histograma mostra a frequência de lançamentos em diferentes anos.
print("\nGerando gráfico: Distribuição de Lançamentos por Ano")
fig_release_year = px.histogram(
    df,
    x='release_year',
    nbins=20, # Número de "caixas" para o histograma
    title='Distribuição de Lançamentos por Ano',
    labels={'release_year': 'Ano de Lançamento', 'count': 'Número de Jogos'},
    template='plotly_white' # Define um tema para o gráfico
)
fig_release_year.show()
fig_release_year.write_html("release_year_distribution.html") # Salva o gráfico como HTML

# 2.3. Distribuição de Lançamentos por Mês
# Convertendo o número do mês para o nome do mês para melhor legibilidade.
print("\nGerando gráfico: Contagem de Jogos por Mês de Lançamento")
df['release_month_name'] = df['release_month'].apply(lambda x: calendar.month_name[x])
# Para garantir a ordem correta dos meses, podemos usar uma categoria ordenada
month_order = [calendar.month_name[i] for i in range(1, 13)]
df['release_month_name'] = pd.Categorical(df['release_month_name'], categories=month_order, ordered=True)

release_month_counts = df['release_month_name'].value_counts().sort_index().reset_index()
release_month_counts.columns = ['month', 'count'] # Renomeando as colunas

fig_release_month = px.bar(
    release_month_counts,
    x='month',
    y='count',
    title='Contagem de Jogos por Mês de Lançamento',
    labels={'month': 'Mês de Lançamento', 'count': 'Número de Jogos'},
    color='month',
    category_orders={'month': month_order} # Garante a ordem dos meses no gráfico
)
fig_release_month.show()
fig_release_month.write_html("release_month_count.html") # Salva o gráfico como HTML

# 2.4. Distribuição de Preços (Dólar e Euro)
# Histograma para ver a forma da distribuição e box plot para estatísticas descritivas (mediana, quartis, outliers).
print("\nGerando gráficos: Distribuição de Preços (Dólar e Euro)")
fig_price_dolar_hist = px.histogram(
    df,
    x='preco_dolar',
    nbins=30,
    title='Distribuição de Preços em Dólar',
    labels={'preco_dolar': 'Preço (Dólar)', 'count': 'Número de Jogos'},
    marginal='box' # Adiciona um box plot marginal
)
fig_price_dolar_hist.show()
fig_price_dolar_hist.write_html("price_dolar_distribution.html") # Salva o gráfico como HTML

fig_price_euro_hist = px.histogram(
    df,
    x='preco_euro',
    nbins=30,
    title='Distribuição de Preços em Euro',
    labels={'preco_euro': 'Preço (Euro)', 'count': 'Número de Jogos'},
    marginal='violin' # Adiciona um violin plot marginal
)
fig_price_euro_hist.show()
fig_price_euro_hist.write_html("price_euro_distribution.html") # Salva o gráfico como HTML

# 2.5. Análise de Gêneros
# Somar as colunas booleanas para obter a contagem de jogos por gênero.
print("\nGerando gráfico: Contagem de Jogos por Gênero")
genre_columns = [col for col in df.columns if col.startswith('genre_')]
genre_counts = df[genre_columns].sum().sort_values(ascending=False)

fig_genre_counts = px.bar(
    x=genre_counts.index.str.replace('genre_', ''), # Remove o prefixo 'genre_'
    y=genre_counts.values,
    title='Contagem de Jogos por Gênero',
    labels={'x': 'Gênero', 'y': 'Número de Jogos'},
    color=genre_counts.index.str.replace('genre_', '')
)
fig_genre_counts.show()
fig_genre_counts.write_html("genre_counts.html") # Salva o gráfico como HTML

# --- 3. Análise Bivariada e Multivariada ---

# 3.1. Preço Médio por Plataforma
# Usando box plots para comparar a distribuição de preços entre plataformas.
print("\nGerando gráfico: Distribuição de Preços por Plataforma (Dólar)")
fig_price_by_platform = px.box(
    df,
    x='platform',
    y='preco_dolar',
    title='Distribuição de Preços (Dólar) por Plataforma',
    labels={'platform': 'Plataforma', 'preco_dolar': 'Preço (Dólar)'},
    color='platform'
)
fig_price_by_platform.show()
fig_price_by_platform.write_html("price_by_platform.html") # Salva o gráfico como HTML

# 3.2. Tendência de Preço ao Longo dos Anos
# Gráfico de dispersão para ver a relação entre o ano de lançamento e o preço.
print("\nGerando gráfico: Preço (Dólar) ao Longo dos Anos")
fig_price_year_scatter = px.scatter(
    df,
    x='release_year',
    y='preco_dolar',
    title='Preço (Dólar) ao Longo dos Anos',
    labels={'release_year': 'Ano de Lançamento', 'preco_dolar': 'Preço (Dólar)'},
    hover_data=['title', 'platform'], # Mostra título e plataforma ao passar o mouse
    trendline='ols' # Adiciona uma linha de tendência (Ordinary Least Squares)
)
fig_price_year_scatter.show()
fig_price_year_scatter.write_html("price_year_scatter.html") # Salva o gráfico como HTML

# 3.3. Preço Médio por Gênero
# Usando um gráfico de barras para o preço médio por gênero.
print("\nGerando gráfico: Preço Médio (Dólar) por Gênero")
# Criar um DataFrame 'long-form' para facilitar a plotagem de múltiplos gêneros
df_genres_melted = df.melt(
    id_vars=['preco_dolar'],
    value_vars=genre_columns,
    var_name='genre_full',
    value_name='is_genre'
)
df_genres_melted = df_genres_melted[df_genres_melted['is_genre'] == True]
df_genres_melted['genre'] = df_genres_melted['genre_full'].str.replace('genre_', '')

avg_price_by_genre = df_genres_melted.groupby('genre')['preco_dolar'].mean().sort_values(ascending=False).reset_index()

fig_avg_price_genre = px.bar(
    avg_price_by_genre,
    x='genre',
    y='preco_dolar',
    title='Preço Médio (Dólar) por Gênero',
    labels={'genre': 'Gênero', 'preco_dolar': 'Preço Médio (Dólar)'},
    color='genre'
)
fig_avg_price_genre.show()
fig_avg_price_genre.write_html("avg_price_by_genre.html") # Salva o gráfico como HTML

# 3.4. Top 10 Desenvolvedores por Número de Jogos
# Para colunas com muitos valores únicos como 'developers' ou 'publishers', é bom focar nos top N.
print("\nGerando gráfico: Top 10 Desenvolvedores por Número de Jogos")
top_developers = df['developers'].value_counts().head(10).reset_index()
top_developers.columns = ['Developer', 'Count']

fig_top_devs = px.bar(
    top_developers,
    x='Developer',
    y='Count',
    title='Top 10 Desenvolvedores por Número de Jogos',
    labels={'Developer': 'Desenvolvedor', 'Count': 'Número de Jogos'},
    color='Developer'
)
fig_top_devs.show()
fig_top_devs.write_html("top_developers.html") # Salva o gráfico como HTML

# 3.5. Scatter Plot com Múltiplas Variáveis (Ano, Preço, Plataforma)
# Usando cor para uma terceira variável categórica.
print("\nGerando gráfico: Preço (Dólar) vs. Ano de Lançamento por Plataforma")
fig_scatter_multi = px.scatter(
    df,
    x='release_year',
    y='preco_dolar',
    color='platform', # Colore os pontos pela plataforma
    size='preco_dolar', # O tamanho do ponto reflete o preço
    hover_name='title', # Título do jogo aparece ao passar o mouse
    title='Preço (Dólar) vs. Ano de Lançamento por Plataforma',
    labels={'release_year': 'Ano de Lançamento', 'preco_dolar': 'Preço (Dólar)'},
    animation_frame='release_year', # Cria uma animação ao longo dos anos (útil para grandes datasets)
    animation_group='platform',
    range_x=[df['release_year'].min() - 1, df['release_year'].max() + 1],
    range_y=[0, df['preco_dolar'].max() + 10]
)
# Para animação, pode ser necessário ajustar o passo e a velocidade
fig_scatter_multi.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 200
fig_scatter_multi.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 100
fig_scatter_multi.show()
fig_scatter_multi.write_html("price_year_platform_scatter.html") # Salva o gráfico como HTML

# --- 4. Exemplo de uso de plotly.graph_objects para maior controle ---
# Criando um gráfico de linhas para o número de lançamentos por ano (mais controle sobre traces)
print("\nGerando gráfico: Número de Lançamentos por Ano (go.Figure)")
yearly_releases = df['release_year'].value_counts().sort_index().reset_index()
yearly_releases.columns = ['Year', 'Count']

fig_go_line = go.Figure()
fig_go_line.add_trace(go.Scatter(
    x=yearly_releases['Year'],
    y=yearly_releases['Count'],
    mode='lines+markers',
    name='Número de Lançamentos',
    line=dict(color='royalblue', width=2),
    marker=dict(size=8, color='lightskyblue', line=dict(width=1, color='DarkSlateGrey'))
))

fig_go_line.update_layout(
    title='Número de Lançamentos de Jogos por Ano',
    xaxis_title='Ano de Lançamento',
    yaxis_title='Número de Jogos',
    hovermode='x unified' # Melhora a interatividade ao passar o mouse
)
fig_go_line.show()
fig_go_line.write_html("yearly_releases_line.html") # Salva o gráfico como HTML

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

# --- 6. Gráfico Sunburst para Análise Hierárquica ---
print("\nGerando gráfico: Sunburst de Ano, Plataforma e Gênero")

# Preparar os dados para o Sunburst
# Precisamos de um DataFrame onde cada linha representa uma combinação única de ano, plataforma e gênero
# e a contagem de jogos para essa combinação.

# 1. Derreter as colunas de gênero para formato longo
df_sunburst = df.melt(
    id_vars=['release_year', 'platform'],
    value_vars=genre_columns,
    var_name='genre_full',
    value_name='is_genre'
)

# 2. Filtrar apenas os registros onde o gênero é verdadeiro
df_sunburst = df_sunburst[df_sunburst['is_genre'] == True]

# 3. Remover o prefixo 'genre_' do nome do gênero
df_sunburst['genre'] = df_sunburst['genre_full'].str.replace('genre_', '')

# 4. Contar ocorrências para cada caminho hierárquico
# O Plotly Express Sunburst pode fazer a contagem automaticamente se você passar os caminhos.
# No entanto, para garantir que todos os níveis sejam considerados e para ter um 'values' explícito,
# podemos agrupar e contar.
sunburst_data = df_sunburst.groupby(['release_year', 'platform', 'genre']).size().reset_index(name='count')

fig_sunburst = px.sunburst(
    sunburst_data,
    path=['release_year', 'platform', 'genre'], # Define a hierarquia dos níveis
    values='count', # Define o valor que determina o tamanho de cada segmento
    title='Distribuição de Jogos por Ano, Plataforma e Gênero',
    color='genre', # Colore os segmentos finais pelo gênero
    hover_data=['count'] # Mostra a contagem ao passar o mouse
)

fig_sunburst.show()
fig_sunburst.write_html("sunburst_chart.html") # Salva o gráfico como HTML
