import pandas as pd
import plotly.express as px
import os
import re

# --- Carregamento do DataFrame ---
caminho_arquivo = os.path.join(r"E:\UFRN 2025_1\CIENCIA DE DADOS\tarefa1\trabalhoP2\DB_completo_plataformas.csv")
data = pd.read_csv(caminho_arquivo)
df = pd.DataFrame(data)

print("DataFrame carregado com sucesso.")
print(df.head())
print(df.info())
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

# --- 3.2. Tendência de Preço ao Longo dos Anos ---
print("\nGerando gráfico: Preço (Dólar) ao Longo dos Anos")
try:
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
except KeyError as e:
    print(f"Erro: Coluna não encontrada para o gráfico de preço ao longo dos anos: {e}. Verifique 'release_year', 'preco_dolar', 'title', 'platform'.")
except UnicodeEncodeError as e:
    print(f"Erro de codificação Unicode ao gerar o gráfico de preço ao longo dos anos: {e}")
except Exception as e:
    print(f"Erro ao gerar o gráfico de preço (Dólar) ao longo dos anos: {e}")