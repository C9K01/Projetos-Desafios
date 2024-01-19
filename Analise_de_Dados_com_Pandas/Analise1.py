import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Criar dados fictícios
dados = {
    'Produto': ['Produto A', 'Produto B', 'Produto C', 'Produto D', 'Produto E'],
    'Quantidade_Vendida': [150, 200, 120, 180, 250],
    'Preco_Unitario': [10.5, 15.25, 8.99, 12.75, 9.99],
    'Categoria': ['Eletrônicos', 'Roupas', 'Eletrônicos', 'Roupas', 'Acessórios']
}

# Criar DataFrame
df = pd.DataFrame(dados)

# Exibir as primeiras linhas do DataFrame
print(df.head())

# Resumo estatístico
print("\nResumo Estatístico:")
print(df.describe())

# Visualizar a relação entre a quantidade vendida e o preço unitário
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Quantidade_Vendida', y='Preco_Unitario', hue='Categoria')
plt.title('Relação entre Quantidade Vendida e Preço Unitário por Categoria')
plt.xlabel('Quantidade Vendida')
plt.ylabel('Preço Unitário')
plt.show()

# Visualizar a contagem de produtos por categoria
plt.figure(figsize=(8, 6))
sns.countplot(data=df, x='Categoria')
plt.title('Contagem de Produtos por Categoria')
plt.xlabel('Categoria')
plt.ylabel('Contagem')
plt.show()
