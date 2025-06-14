import pandas as pd
import plotly.express as px

# Carregar seu DataFrame
data = pd.read_csv(r"E:\UFRN 2025_1\CIENCIA DE DADOS\tarefa1\trabalhoP2\DB_completo_plataformas.csv")
df = pd.DataFrame(data)

print("DataFrame carregado.")
print(df.head())
print(df.columns)

print("\nGerando gráfico: Preço Médio (Dólar) por Gênero")
try:
    # Definir genre_columns AQUI, antes de usá-la
    genre_columns = [col for col in df.columns if col.startswith('genre_')]

    if not genre_columns:
        print("Aviso: Nenhuma coluna de gênero encontrada.")
    else:
        # Criar um DataFrame 'long-form' para facilitar a plotagem de múltiplos gêneros
        df_genres_melted = df.melt(
            id_vars=['preco_dolar'],
            value_vars=genre_columns,
            var_name='genre_full',
            value_name='is_genre'
        )
        df_genres_melted = df_genres_melted[df_genres_melted['is_genre'] == True]
        df_genres_melted['genre'] = df_genres_melted['genre_full'].str.replace('genre_', '')

        avg_price_by_genre = df_genres_melted.groupby('genre')['preco_dolar'].mean().sort_values(ascending=False).reset_index()

        fig_avg_price_genre = px.bar(
            avg_price_by_genre,
            x='genre',
            y='preco_dolar',
            title='Preço Médio (Dólar) por Gênero',
            labels={'genre': 'Gênero', 'preco_dolar': 'Preço Médio (Dólar)'},
            color='genre'
        )
        fig_avg_price_genre.show()
        fig_avg_price_genre.write_html("avg_price_by_genre.html") # Salva o gráfico como HTML

except KeyError as e:
    print(f"Erro de KeyError: {e}. Verifique os nomes das colunas no DataFrame.")
except Exception as e:
    print(f"Erro ao gerar o gráfico de preço médio por gênero: {e}")