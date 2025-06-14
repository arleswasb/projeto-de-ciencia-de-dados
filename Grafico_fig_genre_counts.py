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


# 2.5. Análise de Gêneros
# Somar as colunas booleanas para obter a contagem de jogos por gênero.
print("\nGerando gráfico: Contagem de Jogos por Gênero")
genre_columns = [col for col in df.columns if col.startswith('genre_')] # Mova a definição para fora do try

try:
    if not genre_columns:
        print("Aviso: Nenhuma coluna de gênero (começando com 'genre_') encontrada no DataFrame.")
    else:
        genre_counts = df[genre_columns].sum().sort_values(ascending=False)

        fig_genre_counts = px.bar(
            x=genre_counts.index.str.replace('genre_', ''), # Remove o prefixo 'genre_'
            y=genre_counts.values,
            title='Contagem de Jogos por Gênero',
            labels={'x': 'Gênero', 'y': 'Número de Jogos'},
            color=genre_counts.index.str.replace('genre_', '')
        )
        fig_genre_counts.show()
        fig_genre_counts.write_html("genre_counts.html") # Salva o gráfico como HTML
except Exception as e:
    print(f"Erro ao gerar o gráfico de contagem de jogos por gênero: {e}")