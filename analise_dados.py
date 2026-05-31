import pandas as pd
import re

# ETAPA 1: Carregar a base e exibir informações estruturais -> Início
# ______________________________________________________________________________________

print("INICIANDO A SPRINT 1: IMPORTAÇÃO E ENTENDIMENTO DOS DADOS")

# Carregando a base de dados com pandas
# Usando sep=';' pois é o padrão da base Varejo
caminho_arquivo = 'Base Varejo.csv'
df = pd.read_csv(caminho_arquivo, sep=';')

# Criando uma cópia INDEPENDENTE na memória para preservar o arquivo original
df_trabalhado = df.copy()
print("Cópia isolada em memória (df_trabalhado) criada com sucesso.")

# Extraindo o número de registros (linhas) e colunas para visualizar estrutura do dataframe
num_registros = df_trabalhado.shape[0]
num_colunas = df_trabalhado.shape[1]

# Mostrando os resultados
print(f"\n1. NÚMERO DE REGISTROS: {num_registros}")
print(f"\n2. NÚMERO DE COLUNAS: {num_colunas}")
print(f"\n3. NOME DAS COLUNAS:")
print(list(df_trabalhado.columns))
print(f"\n4. TIPOS DE DADOS POR COLUNA:")
print(df_trabalhado.dtypes)

# Amostra inicial dos dados (df_trabalhado.head)
print("\nAMOSTRA DOS DADOS (df_trabalhado.head()):")
print(df_trabalhado.head())

# Verificação inicial de valores nulos (df_trabalhado.isnull().sum())
print("\nVALORES NULOS POR COLUNA (df_trabalhado.isnull().sum()):")
nulos = df_trabalhado.isnull().sum()
print(nulos[nulos > 0]) # Filtra para exibir apenas colunas que possuem nulos

print("\nFINALIZANDO A SPRINT 1: IMPORTAÇÃO E ENTENDIMENTO DOS DADOS")
# ______________________________________________________________________________________
# ETAPA 1: Carregar a base e exibir informações estruturais -> Fim

# ETAPA 2: Transformação de Strings, Integer, Float e Datetime -> Início
# ______________________________________________________________________________________
print("\nINICIANDO A SPRINT 2: TRANSFORMAÇÕES E LIMPEZA COM REGEX")

# Limpeza Estrutural: Remover colunas "fantasmas" geradas por ;;;; no CSV
# O pandas nomeia colunas sem cabeçalho como 'Unnamed: X'. Vamos filtrá-las.
df_trabalhado = df_trabalhado.loc[:, ~df_trabalhado.columns.str.contains('^Unnamed')]
print("Colunas vazias ('Unnamed') removidas com sucesso.")

# Transformação de Strings com Expressões Regulares (Regex)
def limpar_texto_regex(texto):
    """
    Remove espaços extras (no início, fim e entre as palavras) e 
    força padronização em letras maiúsculas.
    """
    if pd.isna(texto):
        return texto
    # Transforma em string e maiúsculo
    texto_limpo = str(texto).upper().strip()
    # REGEX: Substitui múltiplos espaços em branco por apenas um espaço ' '
    texto_limpo = re.sub(r'\s+', ' ', texto_limpo)
    return texto_limpo

# Aplicando a função nas colunas de texto
colunas_texto = ['CL_GENERO', 'CL_SEG', 'PR_CAT', 'PR_NOME']
for col in colunas_texto:
    df_trabalhado[col] = df_trabalhado[col].apply(limpar_texto_regex)
    
print("Limpeza de texto (Strings) realizada utilizando Regex.")

# Transformação de Integer e Float
# Convertendo IDs numéricos e número de filhos. errors='coerce' transforma lixo em NaN
colunas_numericas = ['CO_ID', 'CL_ID', 'CL_EC', 'CL_FHL', 'PR_ID']
for col in colunas_numericas:
    df_trabalhado[col] = pd.to_numeric(df_trabalhado[col], errors='coerce')
    
print("Conversão de atributos numéricos (Integer/Float) concluída.")

# Transformação de Datetime
# Convertendo a string da data para o formato datetime do Pandas (Dia/Mês/Ano)
df_trabalhado['DATA'] = pd.to_datetime(df_trabalhado['DATA'], format='%d/%m/%Y', errors='coerce')
print("Conversão da coluna 'DATA' para datetime finalizada.")

# Verificando os valores após as transformações
print("\n-> TIPOS DE DADOS APÓS AS TRANSFORMAÇÕES (df_trabalhado.dtypes):")
print(df_trabalhado.dtypes)
print("\n-> AMOSTRA DOS DADOS LIMPOS (df_trabalhado.head()):")
print(df_trabalhado.head())

print("\nFINALIZANDO A SPRINT 2: TRANSFORMAÇÕES E LIMPEZA COM REGEX")
# ______________________________________________________________________________________
# ETAPA 2: Transformação de Strings, Integer, Float e Datetime -> Fim
