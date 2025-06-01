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
