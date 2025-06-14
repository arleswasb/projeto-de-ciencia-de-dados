import pandas as pd
import plotly.express as px
import os
import re

# --- Carregamento do DataFrame ---
caminho_arquivo = os.path.join(r"E:\UFRN 2025_1\CIENCIA DE DADOS\tarefa1\trabalhoP2\DB_completo_plataformas.csv")
data = pd.read_csv(caminho_arquivo)
df = pd.DataFrame(data)

print("DataFrame de exemplo criado com sucesso. Primeiras 5 linhas:")
print(df.head())
print("\nInformações do DataFrame:")
df.info()
print("-" * 50)

# --- Correção para UnicodeEncodeError - Remoção de não ASCII ---
def remove_non_ascii(text):
    if isinstance(text, str):
        return re.sub(r'[^\x00-\x7F]+', '', text)
    return text

try:
    df['title'] = df['title'].apply(remove_non_ascii)
    df['platform'] = df['platform'].apply(remove_non_ascii)
    print("Caracteres não ASCII removidos das colunas 'title' e 'platform'.")
except Exception as e:
    print(f"Erro ao tentar remover caracteres não ASCII: {e}")

# --- 3.5. Scatter Plot com Múltiplas Variáveis (Ano, Preço, Plataforma) ---
print("\nGerando gráfico: Preço (Dólar) vs. Ano de Lançamento por Plataforma")
try:
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
except KeyError as e:
    print(f"Erro: Coluna não encontrada para o gráfico de dispersão multi-variável: {e}. Verifique 'release_year', 'preco_dolar', 'platform', 'title'.")
except Exception as e:
    print(f"Erro ao gerar o gráfico de dispersão com múltiplas variáveis: {e}")