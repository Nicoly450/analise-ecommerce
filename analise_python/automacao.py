import pandas as pd
import os 
from sqlalchemy import create_engine

#Localiza o CSV mais recente da pasta anterior
pasta = '.'
arquivos = [arq for arq in os.listdir(pasta) if arq.endswith('.csv')]
arquivo_recente = max(arquivos, key=lambda x: os.path.getctime(os.path.join(pasta, x)))
caminho = os.path.join(pasta, arquivo_recente)

print(f"Lendo arquivo mais recente: {arquivo_recente}")
df = pd.read_csv(caminho)

# 1. Corrige valores inconsistentes nas colunas especificas
df['canal'] = df['canal'].replace({'insta': 'Instagram'})
df['forma_pagamento'] = df['forma_pagamento'].replace({'dinher': 'Dinheiro', 'cartao': 'Cartão'})

# 2. Limpeza genérica dos dados (aplicada a qualquer tabela)
for coluna in df.columns:
    if df[coluna].dtype == 'object':
     
     # Padronização capitalização e remove espaços extras
     df[coluna] = df[coluna].str.title().str.strip()

     # Substitui "não informado" por vazio (NaN) p/ evitar distorções na análise
     df[coluna] = df[coluna].replace(['não informado', 'não informado!', 'Não informado!'], pd.NA)
    

# 3. Conecta ao banco MySQL via SQLAlchemy
usuario = 'root'
senha = 'ocultado'
host = 'localhost'
banco = 'limpeza'
engine = create_engine(f'mysql+pymysql://{usuario}:{senha}@{host}/{banco}')

# 5. Define o nome da tabela com base no nome do arquivo
nome_arquivo = os.path.splitext(arquivo_recente)[0]
nome_tabela = nome_arquivo.lower().replace('.', '_').replace('-', '_')

# 6. Salva os dados limpos no banco com esse nome de tabela
df.to_sql(name=nome_tabela, con=engine, if_exists='replace', index=False)

# 7. Salvar localmente
df.to_csv(f'{nome_arquivo}.limpos.csv', index=False)

print(f"✅ Automação concluída: tabela '{nome_tabela}' criada e arquivo salvo como '{nome_arquivo}.limpos.csv'")
