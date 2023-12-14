# Pipeline de Detecção de Anomalias

# Imports
import os
import numpy as np
from google.cloud import bigquery

print("\nPipeline de Detecção de Anomalias em DW!")

# Define o caminho para o arquivo de credenciais (coloque o caminho da chave no seu computador)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'caminho da chave'

print("\nService Account KEY:", os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

# Cria o cliente
client = bigquery.Client()

# Define a query
query = """
   	SELECT Nome, sum(Quantidade) as Total_Quantidade
    FROM `database_retail_store.DIMENSAO_PRODUTO` as A, `database_retail_store.FATO_VENDA` as C
    WHERE A.Produto_ID = C.Produto_ID
    GROUP BY Nome
    ORDER BY Nome
"""

# Executa a query no DW
query_job = client.query(query)

# Inicializa lista e dicionário
total_unidades = []
dict_prod_unidades = {}

print("\nTotal de Unidades Vendidas Por Produto:\n")

# Loop pela query para extrair os dados
for row in query_job:
    print("produto={}, total_unidades_vendidas={}".format(row[0], row["Total_Quantidade"]))
    total_unidades.append(row["Total_Quantidade"])
    dict_prod_unidades[row[0]] = row["Total_Quantidade"]

# Calculando Q1, Q3 e IQR
Q1 = np.percentile(total_unidades, 25)
Q3 = np.percentile(total_unidades, 75)
IQR = Q3 - Q1

# Definindo os limites para as anomalias
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Identificando as anomalias
print("\nIdentificando Anomalias...")
anomalias = [unidades for unidades in total_unidades if unidades < lower_bound or unidades > upper_bound]

print('\nTotal de Unidades Vendidas Que Podem Indicar Uma Anomalia: ', anomalias)

# Loop
for chave, valor in dict_prod_unidades.items():
    for elemento in anomalias:
        if valor == elemento:
            print("Produto(s) com Total de Unidades Vendidas Representando Uma Anomalia:", chave)

print("\nPipeline Concluído com Sucesso!\n")






