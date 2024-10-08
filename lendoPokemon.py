import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def bar_plot(df: pd.DataFrame, eixo_x: str, eixo_y: str, titulo: str) -> None:

    ax = sns.barplot(x=eixo_x, y=eixo_y, data=df, palette="Set3")

    # Add labels and title
    plt.xlabel(eixo_x)
    plt.ylabel(eixo_y)

    for p in ax.patches:
        ax.text(p.get_x() + p.get_width() / 2., p.get_height(), f'{int(p.get_height())}',
                ha='center', va='bottom', fontsize=10, color='black')

    plt.xticks(rotation=90)

    plt.title(titulo)

    # Show the plot
    plt.show()
df_pokemon = pd.read_csv('./pokemon.csv', sep=',').drop(columns=['Total', '#'])
df_pokemon.head()
# Resposta da Pergunta 0:
  # A coluna 'Type 2' possui valores nulos;
  # Não há linhas duplicadas.

df_pokemon.info()
print(f"Linhas duplicadas: {df_pokemon.duplicated().sum()}")

df_pokemon = df_pokemon[~df_pokemon.duplicated()]

print(f"Linhas duplicadas: {df_pokemon.duplicated().sum()}")

df_pokemon
# Pergunta 1- Qual o tipo de pokémon mais presente no dataset? (considere as duas colunas para isso);

# verificar se há valroes duplicados nas colunas 'Type 1 e Type 2'
print(f"Total de colunas 'Type 1' e 'Type 2' com valores duplicados: {len(df_pokemon[df_pokemon['Type 1'] == df_pokemon['Type 2']])}")

# criar uma nova coluna 'Type' a partir da unificação de 'Type 1' e 'Type 2'.
df_pokemon['Type 2'] = df_pokemon['Type 2'].fillna('')

# Removendo '/' que sobra nos tipos quando o pokemon possui apenas o 'Type 1'.
df_pokemon['Type'] = np.where(df_pokemon['Type 2'] == '', df_pokemon['Type 1'],
                              df_pokemon['Type 1'] + '/' + df_pokemon['Type 2'])

# Remove as colunas 'Type 1', 'Type 2'.
df_pokemon = df_pokemon.drop(columns=['Type 1', 'Type 2'])

dfpc = df_pokemon["Type"].value_counts(ascending=False).reset_index().head(10)
dfpc = dfpc.rename(columns={"Type": "Tipo", "count": "Total"})

bar_plot(dfpc, dfpc.columns[0], dfpc.columns[1], 'Top 10 categorias mais frequentes de Pokémons')
# Pergunta 3: Liste os 10 pokémons mais poderosos a partir de uma medida de agregação.

df_pokemon["Power"] = df_pokemon[["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]].sum(axis=1)
dfpp = df_pokemon[["Name", "Power"]].sort_values(by="Power", ascending=False).head(10)

bar_plot(dfpp, dfpp.columns[0], dfpp.columns[1], 'Top 10 Pokémons mais poderosos')


# EXERCÍCIO: TRANSFORMAR O GRÁFICO ABAIXO EM UM GRÁFICO DE BARRAS SECCIONADO, UTILIZANDO OS ATRIBUTOS SOMADOS.
# Pergunta 5. Liste os pokemóns mais poderosos por tipo (considere as duas colunas para isso);

df_poder_categoria = df_pokemon.groupby(by='Type')[["Type", "Name", "Power"]].apply(lambda x: x.sort_values(by='Power', ascending=False).head(1)).reset_index(drop=True)
df_poder_categoria = df_poder_categoria.sort_values(by='Power', ascending=False).head(10)

plt.figure(figsize=(25, 12))
bar_plot_sns = sns.barplot(x='Power', y='Name', hue='Type', data=df_poder_categoria, dodge=False, palette="Set3")

# Adicionar os valores das barras
for index, value in enumerate(df_poder_categoria['Power']):
    plt.text(value + 5, index, str(value), color='black', va="center")

plt.title('Pokémons Mais Poderosos por Tipo')
plt.xlabel('Power')
plt.ylabel('Nome')
plt.show()


# 5. Os pokémons lendários são, em média, mais fortes ou mais fracos que os pokémons normais?
pokemon_lendario = df_pokemon[df_pokemon["Legendary"] == True]
pokemon_normal = df_pokemon[df_pokemon["Legendary"] == False]


poder_lendario = pokemon_lendario['Power'].mean()
poder_normal = pokemon_normal['Power'].mean()


print(f"Média de força dos pokemons Lendários:  {poder_lendario} \n")
print(f"Média de força dos pokemons Normais:  {poder_normal} \n")

poder_lendario>poder_normal


print(poder_lendario)

# 6. Liste, por categoria, a média das habilidades dos pokémons;


pokemons = df_pokemon[["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]].sum(axis=1)

print(df_pokemon['Type 1'])

print(pokemons)
### Perguntas e Tarefas:

# 0. Explore os atributos do dataset e procure por valores nulos e duplicados;
# 1. Qual o tipo de pokémon mais presente no dataset? (considere as duas colunas para isso);
# 2. Exiba em um gráfico a quantidade de pokémons por tipo (considere as duas colunas para isso);
# 3. Liste os 10 pokémons mais poderosos a partir de uma medida de agregação;
# 4. Liste os pokemóns mais poderosos por tipo (considere as duas colunas para isso);
# 5. Os pokémons lendários são, em média, mais fortes ou mais fracos que os pokémons normais?
# 6. Liste, por categoria, a média das habilidades dos pokémons;

