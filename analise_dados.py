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

# ETAPA 3: Limpeza de Nulos, Duplicatas e Otimização de Atributos -> Início
# ______________________________________________________________________________________
print("\nINICIANDO A SPRINT 3: LIMPEZA DE NULOS, DUPLICATAS E OTIMIZAÇÃO DE ATRIBUTOS")

# Tratamento de Nulos e Lógica Condicional
def preencher_categoria(cat):
    """Lógica if/else exigida para preencher categorias vazias"""
    if pd.isna(cat) or str(cat).strip() == "":
        return "SEM CATEGORIA"
    else:
        return cat

df_trabalhado['PR_CAT'] = df_trabalhado['PR_CAT'].apply(preencher_categoria)
print("Condicional aplicada: Valores vazios em 'PR_CAT' substituídos por 'SEM CATEGORIA'.")
# Justificativa técnica: Tratar corretamente os nulos das dimensões físicas, justificando a escolha.."
print(" -> JUSTIFICATIVA: A base 'Varejo' não possui colunas de dimensões físicas (peso, altura, etc.). O tratamento de nulos foi focado nas variáveis de negócio.")

# Regras de Negócio e Datas
# Validação da regra do identificador de número de compra separando registros nulos
nulos_antes = df_trabalhado.shape[0]
df_trabalhado.dropna(subset=['CO_ID'], inplace=True)
registros_removidos = nulos_antes - df_trabalhado.shape[0]
print(f"\nRegra de Negócio: {registros_removidos} registros com ID de Compra (CO_ID) nulo foram removidos.")

# Limpeza de Duplicatas
duplicatas = df_trabalhado.duplicated().sum()
print(f"\nForam encontradas {duplicatas} linhas duplicadas na base. Como não há um ID único para cada produto, a remoção de duplicatas é necessária para garantir a qualidade dos dados.")
if duplicatas > 0:
    df_trabalhado.drop_duplicates(inplace=True)
    print(" -> Duplicatas removidas com sucesso.")

# Seleção de Atributos (Remoção de Colunas Irrelevantes para os Objetivos)
# Mapeamento técnico: CL_EC (Estado Civil) não possui aderência aos objetivos de entrega
if 'CL_EC' in df_trabalhado.columns:
    df_trabalhado.drop(columns=['CL_EC'], inplace=True)
    print("\nOtimização: Coluna 'CL_EC' (Estado Civil) removida por não possuir mapeamento com os objetivos do desafio e ocupar memória desnecessariamente.")

# Verificando os valores após a limpeza de nulos e duplicatas
print("\nRESUMO APÓS A SPRINT 3 (QUALIDADE DOS DADOS):")
print(f"\nColunas e valores finais:\n{df_trabalhado.head()}")
print(f"\nValores nulos por coluna:\n{df_trabalhado.isnull().sum()}")
print(f"\nRegistros finais limpos e prontos para análise: {df_trabalhado.shape[0]}")
print("\nFINALIZANDO A SPRINT 3: LIMPEZA DE NULOS, DUPLICATAS E OTIMIZAÇÃO DE ATRIBUTOS")
# ______________________________________________________________________________________
# ETAPA 3: Limpeza de Nulos, Duplicatas e Otimização de Atributos -> Fim

# ETAPA 4: Estatística Descritiva -> Início
# ______________________________________________________________________________________
print("\nINICIANDO A SPRINT 4: ESTATÍSTICA DESCRITIVA (CL_FHL)")

# Isolando a variável de interesse
# Utilizado dropna() apenas por segurança matemática, garantindo que o cálculo não quebre
serie_filhos = df_trabalhado['CL_FHL'].dropna()

# Aplicando as funções estatísticas para obter os parâmetros solicitados
estatisticas_filhos = {
    "Contagem": serie_filhos.count(),
    "Média": round(serie_filhos.mean(), 2),
    "Mediana": serie_filhos.median(),
    "Moda": serie_filhos.mode()[0],  # .mode() retorna uma Series, o [0] extrai o número real
    "Desvio Padrão": round(serie_filhos.std(), 2),
    "Mínimo": serie_filhos.min(),
    "Máximo": serie_filhos.max(),
    "1º Quartil (25%)": serie_filhos.quantile(0.25),
    "3º Quartil (75%)": serie_filhos.quantile(0.75)
}

# Exibindo o relatório no terminal
print("Parâmetros Estatísticos - Número de filhos dos clientes (CL_FHL):")
for metrica, valor in estatisticas_filhos.items():
    print(f" -> {metrica}: {valor}")

# Justificativa/Insight Técnico
print("\n -> INSIGHT ESTATÍSTICO: A diferença entre a Média e a Mediana, junto com o Desvio Padrão, ajuda a entender que a base de clientes é formada predominantemente por indivíduos sem filhos.")
print("\n -> INSIGHT MERCADOLÓGICO: O varejo pode focar em produtos para adultos e jovens.")
print("\nFINALIZANDO A SPRINT 4: ESTATÍSTICA DESCRITIVA (CL_FHL)")

# ______________________________________________________________________________________
# ETAPA 4: Estatística Descritiva -> Fim

# ETAPA 5: Padrões de Agrupamento -> Início
# ______________________________________________________________________________________
print("\nINICIANDO A SPRINT 5: PADRÕES DE AGRUPAMENTO (GROUPBY) E COMBINAÇÕES")

# Agrupamento 1: Volume de Compras Únicas por Gênero
# Objetivo: Responder "quem compra mais?"
compras_por_genero = df_trabalhado.groupby('CL_GENERO')['CO_ID'].nunique().sort_values(ascending=False)
print("\n1. Volume de Compras Únicas por Gênero:")
print(compras_por_genero)
print(" -> INSIGHT 1: Este dado revela qual gênero possui a maior taxa de conversão (idas ao caixa), direcionando campanhas de marketing.")

# Agrupamento 2: Top Categorias Mais Vendidas (Volume de Itens)
# Objetivo: Responder "quais categorias vendem mais?"
vendas_por_categoria = df_trabalhado.groupby('PR_CAT')['PR_ID'].count().sort_values(ascending=False)
print("\n2. Top 5 Categorias com Maior Volume de Itens Vendidos:")
print(vendas_por_categoria.head(5))
print(" -> INSIGHT 2: Aponta a 'Curva A' de produtos da loja, fundamental para a gestão de estoque e reposição.")

# Agrupamento 3: Vendas ao Longo do Tempo (Mensal)
# Objetivo: Responder "como variam as vendas ao longo do tempo?" 
df_trabalhado['ANO_MES'] = df_trabalhado['DATA'].dt.to_period('M')
vendas_por_mes = df_trabalhado.groupby('ANO_MES')['CO_ID'].nunique().sort_values(ascending=False)
print("\n3. Top 5 Meses com Maior Fluxo de Compras (Sazonalidade):")
print(vendas_por_mes.head(5))
print(" -> INSIGHT 3: Identifica os picos sazonais de venda, auxiliando no planejamento financeiro e contratação de temporários.")

# IMPLEMENTAÇÃO DAS COMBINAÇÕES
print("\nCOMBINAÇÕES DE AGRUPAMENTOS E VARIÁVEIS PARA EXPLORAÇÃO DE PADRÕES CRUZADOS:")

# Combinação 1: Tabela Dinâmica (Gênero x Categoria)
combinacao_genero_categoria = pd.pivot_table(
    df_trabalhado, 
    values='PR_ID',           
    index='PR_CAT',           
    columns='CL_GENERO',      
    aggfunc='count',          
    fill_value=0              
)
combinacao_genero_categoria['TOTAL'] = combinacao_genero_categoria.sum(axis=1)
combinacao_genero_categoria = combinacao_genero_categoria.sort_values(by='TOTAL', ascending=False)
print("\n4. COMBINAÇÃO 1: Tabela Dinâmica de Vendas por Categoria e Gênero (Top 5):")
print(combinacao_genero_categoria.head(5))

# Combinação 2: Agrupamento Duplo (Tempo x Segmento)
compras_tempo_segmento = df_trabalhado.groupby(['ANO_MES', 'CL_SEG'])['CO_ID'].nunique().unstack(fill_value=0)
print("\n5. COMBINAÇÃO 2: Fluxo de Compras por Tempo e Segmento (Últimos 3 meses):")
print(compras_tempo_segmento.tail(3))

# Limpeza: Remover a coluna temporária ANO_MES para manter o DataFrame limpo
df_trabalhado.drop(columns=['ANO_MES'], inplace=True)

print("\nFINALIZANDO A SPRINT 5: PADRÕES DE AGRUPAMENTO E COMBINAÇÕES")
# ______________________________________________________________________________________
# ETAPA 5: Padrões de Agrupamento -> Fim

