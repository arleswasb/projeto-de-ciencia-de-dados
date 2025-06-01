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

