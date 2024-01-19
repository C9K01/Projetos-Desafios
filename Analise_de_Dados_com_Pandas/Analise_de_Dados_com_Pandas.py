import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Criar dados fictícios
dados = {
    'Produto': ['Produto A', 'Produto B', 'Produto C', 'Produto D', 'Produto E'],
    'Vendas_Janeiro': [150, 200, 120, 180, 250],
    'Vendas_Fevereiro': [180, 210, 100, 200, 220],
    'Vendas_Marco': [200, 190, 130, 210, 240]
}

# Criar DataFrame
df_vendas = pd.DataFrame(dados)

# Exibir as primeiras linhas do DataFrame
print(df_vendas.head())

# Resumo estatístico
print("\nResumo Estatístico:")
print(df_vendas.describe())

# Calcular a média das vendas por produto
df_vendas['Media_Vendas'] = df_vendas[['Vendas_Janeiro', 'Vendas_Fevereiro', 'Vendas_Marco']].mean(axis=1)

# Visualizar a média das vendas por produto
plt.figure(figsize=(12, 6))
sns.barplot(data=df_vendas, x='Produto', y='Media_Vendas', hue='Produto', palette='Set2', legend=False)
plt.title('Média de Vendas por Produto')
plt.xlabel('Produto')
plt.ylabel('Média de Vendas')
plt.show()
