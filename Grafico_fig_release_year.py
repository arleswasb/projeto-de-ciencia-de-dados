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
