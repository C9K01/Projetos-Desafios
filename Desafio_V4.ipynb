import sqlite3
import pandas as pd

# Criar uma conexão com o banco de dados SQLite (ou criar um novo se não existir)
conn = sqlite3.connect('exemplo_usado_por_pessoas.db')

# Criar uma tabela para armazenar informações de vendas
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Vendas (
        VendaID INTEGER PRIMARY KEY AUTOINCREMENT,
        Data DATE,
        Receita DECIMAL(10, 2),
        Produto TEXT,
        Quantidade INTEGER
    );
''')

# Inserir dados de exemplo na tabela
dados_vendas = {
    'Data': ['2022-01-01', '2022-01-02', '2022-01-03'],
    'Receita': [150.00, 200.00, 180.00],
    'Produto': ['Produto A', 'Produto B', 'Produto C'],
    'Quantidade': [10, 5, 8]
}
df_vendas = pd.DataFrame(dados_vendas)
df_vendas.to_sql('Vendas', conn, index=False, if_exists='replace')

# Consultar dados da tabela
consulta = pd.read_sql_query('SELECT * FROM Vendas;', conn)
print(consulta)

# Commit para salvar as alterações
conn.commit()

# Fechar a conexão com o banco de dados
conn.close()
