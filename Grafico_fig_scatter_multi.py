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

