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
