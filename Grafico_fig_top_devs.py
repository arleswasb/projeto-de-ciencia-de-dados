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



# 3.4. Top 10 Desenvolvedores por Número de Jogos
# Para colunas com muitos valores únicos como 'developers' ou 'publishers', é bom focar nos top N.
print("\nGerando gráfico: Top 10 Desenvolvedores por Número de Jogos")
try:
    top_developers = df['developers'].value_counts().head(10).reset_index()
    top_developers.columns = ['Developer', 'Count']

    fig_top_devs = px.bar(
        top_developers,
        x='Developer',
        y='Count',
        title='Top 10 Desenvolvedores por Número de Jogos',
        labels={'Developer': 'Desenvolvedor', 'Count': 'Número de Jogos'},
        color='Developer'
    )
    fig_top_devs.show()
    fig_top_devs.write_html("top_developers.html") # Salva o gráfico como HTML
except KeyError:
    print("Erro: A coluna 'developers' não foi encontrada no DataFrame. Verifique os nomes das colunas.")
except Exception as e:
    print(f"Erro ao gerar o gráfico dos top 10 desenvolvedores: {e}")