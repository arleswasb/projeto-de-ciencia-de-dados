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

