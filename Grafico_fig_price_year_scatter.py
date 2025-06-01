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

