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

# --- 2. Análise Univariada ---


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