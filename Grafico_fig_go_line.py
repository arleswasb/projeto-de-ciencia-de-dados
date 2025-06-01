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

