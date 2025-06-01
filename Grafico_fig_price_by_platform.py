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

