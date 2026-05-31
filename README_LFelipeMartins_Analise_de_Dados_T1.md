# 📊 Análise de Dados (Mini-projeto)

Este repositório contém o pipeline completo de Análise Exploratória de Dados (EDA) e processamento ETL de uma base de vendas de varejo, desenvolvido em Python utilizando a biblioteca Pandas.

O projeto aplica técnicas de higienização de dados, estatística descritiva e combinações de agrupamento para extrair inteligência de negócios a partir de um histórico de compras.

## 🗄️ Sobre a Base de Dados

Os dados utilizados neste projeto são provenientes de um histórico transacional de varejo. O arquivo bruto (`Base Varejo.csv`) contém dados demográficos de clientes e informações de compra de produtos.

* **Fonte Oficial:** [Base Varejo - Kaggle](https://www.kaggle.com/datasets/namespaiva/base-varejo/data)
* **Formato:** `.csv` (Delimitador: Ponto e vírgula `;`)
* **Volume Inicial:** 830.000 registros e 14 colunas.

## 🛠️ Tecnologias e Ferramentas Utilizadas
- **Python 3:** Linguagem base do projeto.
- **Pandas:** Para modelagem de dados, tratamento de nulos, agregações (`groupby`, `pivot_table`) e ETL.
- **Expressões Regulares (Regex):** Aplicadas via módulo `re` para higienização profunda de strings e padronização.
- **Matplotlib & Seaborn:** Para a construção do dashboard analítico e visualização da sazonalidade.

## 🚀 Como Executar o Projeto

1. Certifique-se de ter o Python e o `pip` instalados no ambiente virtual.
2. Instale as dependências executando o comando:
   ```bash
   pip install pandas matplotlib seaborn

## 🎯 Reflexão Teórica e Insights de Negócio

Após o processamento e a limpeza rigorosa de mais de 830 mil registros brutos, a análise estruturada revelou padrões críticos de consumo que direcionam as decisões estratégicas da loja:

### 1. Lei de Pareto (Curva ABC) e Risco de Ruptura
A análise de agrupamento por categorias revelou uma dependência brutal de um segmento específico do portfólio. A categoria **Alimentos** representa mais de 52% do volume total de itens vendidos na história da loja. Se somada às categorias de Higiene e Limpeza, **três categorias respondem por 88,6% de todo o giro da empresa**. 
* **Ação Estratégica:** O setor de compras deve priorizar o fluxo de caixa para blindar essas categorias contra rupturas (falta de estoque), pois elas sustentam financeiramente o negócio.

### 2. Perfil Familiar e Expansão de Portfólio
A estatística descritiva aplicada à coluna de dependentes (`CL_FHL`) quebrou possíveis suposições empíricas sobre o público. Com a **Mediana e a Moda resultando em 0**, os dados provam que mais de 50% dos clientes ativos da loja não possuem filhos. 
* **Ação Estratégica:** Campanhas de marketing e a introdução de novos produtos devem focar em jovens adultos, solteiros ou casais sem filhos, em vez de investir pesado em vitrines infantis.

### 3. Taxa de Conversão por Gênero
O agrupamento focado em *Ticket/Compras Únicas* (usando o ID do recibo `CO_ID`) demonstrou que o gênero feminino possui uma taxa de conversão (idas ao caixa) superior.
* **Ação Estratégica:** O tom de voz das redes sociais da empresa e o layout visual da loja física devem ser ajustados para engajar primariamente este público de maior aderência.

### 4. Sazonalidade e Gestão de Recursos Humanos
O cruzamento temporal dos dados confirmou que a loja não possui um fluxo linear ao longo dos meses, apresentando picos e vales claros de movimento.
* **Ação Estratégica:** A escala de funcionários (operadores de caixa, repositores) não pode ser estática. As férias e folgas devem ser alocadas nos meses de vale, e a contratação de temporários deve ser engatilhada nos meses que antecedem os picos sazonais apontados no painel.

### 5. O Impacto da Qualidade dos Dados (Data Quality)
Antes de qualquer inferência, o script removeu 96.553 linhas duplicadas e filtrou IDs nulos. 
* **Reflexão Teórica:** Se o processo de ETL (Extração, Transformação e Carga) não tivesse sido aplicado com as regras de negócio corretas, todas as métricas acima estariam corrompidas. O faturamento e o volume de vendas teriam sido reportados de forma irreal para a diretoria, provando que um dado sujo gera uma decisão gerencial equivocada.