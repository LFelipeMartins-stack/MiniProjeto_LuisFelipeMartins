import pandas as pd

# ETAPA 1: Carregar a base e exibir informações estruturais
# __________________________________________________________________

print("--- INICIANDO A SPRINT 1: IMPORTAÇÃO DOS DADOS ---")

# Carregando a base de dados com pandas
# Usando sep=';' pois é o padrão da base Varejo
caminho_arquivo = 'Base Varejo.csv'
df = pd.read_csv(caminho_arquivo, sep=';')

# Extraindo o número de registros (linhas) e colunas
num_registros = df.shape[0]
num_colunas = df.shape[1]

# Mostrando os resultados
print(f"\n1. NÚMERO DE REGISTROS: {num_registros}")
print(f"\n2. NÚMERO DE COLUNAS: {num_colunas}")
print(f"\n3. NOME DAS COLUNAS:")
print(list(df.columns))
print(f"\n4. TIPOS DE DADOS POR COLUNA:")
print(df.dtypes)