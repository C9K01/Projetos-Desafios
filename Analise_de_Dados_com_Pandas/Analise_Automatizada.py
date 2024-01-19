import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Função para obter dados do usuário
def obter_dados():
    produto = input('Nome do Produto: ')
    quantidade_vendida = int(input('Quantidade Vendida: '))
    preco_unitario = float(input('Preço Unitário: '))
    categoria = input('Categoria: ')
    return {'Produto': produto, 'Quantidade_Vendida': quantidade_vendida, 'Preco_Unitario': preco_unitario, 'Categoria': categoria}

# Inicializar DataFrame vazio
df = pd.DataFrame()

# Solicitar ao usuário para inserir dados
resposta = 'S'
while resposta == 'S':
    dados = obter_dados()
    df = pd.concat([df, pd.DataFrame([dados])], ignore_index=True)
    resposta = input('Deseja inserir mais dados? (S/N): ').upper()

# Exibir as primeiras linhas do DataFrame
print('\nDataFrame Atualizado:')
print(df)

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
