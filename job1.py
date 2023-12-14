import os
from google.cloud import bigquery

# Define o caminho para o arquivo de credenciais (coloque o caminho da chave no seu computador)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'caminho da chave'

print("Service Account KEY:", os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

# Cria o cliente
client = bigquery.Client()

# Define a query
query = """
   	SELECT LOJA, avg(Total) as Media_Venda
	FROM `database_retail_store.DIMENSAO_LOCALIDADE` as A, `database_retail_store.FATO_VENDA` as B
	WHERE A.Localidade_ID = B.Localidade_ID
	GROUP BY Loja
"""

# Executa a query no DW
query_job = client.query(query)

print("Dados Extraídos do DW:\n")

# Loop pela query para extrair e imprimir os dados
for row in query_job:
    print("loja={}, media={}".format(row[0], row["Media_Venda"]))