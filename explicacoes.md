
# 📄 Explicações Técnicas do Projeto

Este documento detalha a lógica, funcionamento e os resultados obtidos na **Análise de Performance de Vendas de um E-commerce**, destacando a automação, as análises (SQL + Python) e as visualizações no Power BI.

O projeto foi desenvolvido com foco em simular o dia a dia de um(a) Analista de Dados, integrando limpeza de dados, análise exploratória, extração de insights, visualizações e automações.

---

## ⚙️ Automação de Dados (Python)

Criamos um script de automação chamado `automacao`, responsável por:

- Localizar o arquivo CSV mais recente na pasta do projeto (usando `os`);
- Conexão com o banco de dados MySql (usando `sqlalchemy`)
- Fazer a leitura do arquivo com `pandas`;
- Aplicar uma limpeza genérica, tratando:
  - Espaços em branco nos nomes de colunas e registros;
  - Valores incorretos (ex: escalas erradas por canal ou forma de pagamento);
  - Padronizações (ex: maiúsculas, minúsculas, acentos);
  - Valores como "Não informado" que deveriam representar `NULL`;
- Deixar que o pandas identifique automaticamente os tipos de dados ao ler o arquivo, garantindo que números e datas sejam interpretados corretamente;
- Substituir os valores "Não informado" por `None` (`np.nan`) para não afetar agregações como somas e médias em análises;
- Enviar os dados limpos para o banco de dados MySQL, na tabela `dados2_limpos` dentro do banco `limpeza`, usando SQLAlchemy.

Esse processo garante que, sempre que um novo arquivo for adicionado à pasta, ele será limpo automaticamente e estará pronto para ser analisado com Power BI, SQL ou Python. Tudo isso de forma prática, automática e padronizada.

---

## 🧠 Análises com SQL

As análises com SQL foram realizadas diretamente na tabela `dados2_limpos`, e seus resultados exportados para o Power BI para visualização e interpretação.

### Receita total por canal

```sql
SELECT canal, ROUND(SUM(valor), 2) AS receita_total
FROM dados2_limpos
GROUP BY canal;
```

**Resultado:** O canal com maior receita foi o Ifood, seguido pelo Site. Canais como WhatsApp e Instagram apresentaram menor volume.

**Interpretação:** Ifood e Site são fortes comercialmente. Os outros canais podem ser otimizados com estratégias de marketing.

---

### Quantidade de pedidos por canal

```sql
SELECT Canal, count(*) as 'Quantidade Pedidos' from dados2_limpos
WHERE status = 'Entregue' and status is not null
GROUP BY Canal
ORDER BY count(*) desc;
```

**Resultado:** O canal com mais pedidos foi o iFood, totalizando 33 pedidos.

**Interpretação:** Neste caso, iFood também foi o canal com maior receita, o que mostra um ótimo desempenho tanto em volume quanto em valor. Estratégias como manter promoções ou combos podem ajudar a manter o engajamento nesse canal de alto desempenho.

---

### Ticket médio por canal

```sql
SELECT canal, ROUND(AVG(valor), 2) AS ticket_medio
FROM dados2_limpos
GROUP BY canal;
```

**Resultado:** O Instagram teve o maior ticket médio, seguido por WhatsApp e Site. O iFood ficou com o menor valor médio por pedido.

**Interpretação:** O Instagram atrai clientes com maior poder aquisitivo, o que sugere uma estratégia de marketing mais eficaz nesse canal. Campanhas promocionais direcionadas para o Instagram podem gerar mais receita com menos pedidos, otimizando os resultados da empresa.

---

## 🐍 Análises com Python

As análises em Python foram feitas usando `pandas`, após leitura do CSV e aplicação de filtros e agrupamentos.

### Porcentagem de pedidos cancelados

```python
df_filtrado = df[df['status'].notnull()]
cancelados = df_filtrado[df_filtrado['status'] == 'Cancelado']
percentual_cancelado = (len(cancelados) / len(df_filtrado)) * 100’’’

**Resultado:** Aproximadamente 32,88% dos pedidos foram cancelados.

**Interpretação:** Uma taxa de cancelamento elevada pode indicar problemas com entrega, pagamento ou atendimento. É um alerta importante para ações corretivas.

---

### Ticket médio por cliente

```python
ticket_medio_cliente = df[df['status'] == 'Entregue'].groupby('cliente')['valor'].mean().round(2)
```

**Resultado:** Ticket médio entre R$45,45 e R$53,27. Bruno Mello e Fernanda Rocha estão entre os que mais gastam.


**Interpretação:** Identificar esses clientes permite ações de fidelização (descontos exclusivos, cashback, etc).

---

### Receita total por canal (com pandas)

```python
receita_por_canal = df.groupby('canal')['valor'].sum().sort_values(ascending=False)
```

**Resultado:** Reforça os dados do SQL, com Ifood liderando.

**Interpretação:** Valida que a automatização e limpeza de dados funcionaram corretamente. A análise bate com os valores do SQL e do Power BI.

---

## 📊 Visualizações no Power BI

No Power BI, foram criados dashboards com os seguintes destaques:

- **KPI Total de Receita:** soma de todos os valores válidos (sem `NULL`), filtrados por status "Complete";
- **% de Cancelamento:** cálculo usando medida DAX sobre status "Cancelado";
- **Ticket Médio:** total da receita dividido pela quantidade de pedidos;
- **Participação por Canal:** gráficos de barras e roscas com filtros dinâmicos;
- **Segmentações e Slicers:** para explorar a base por forma de pagamento, canal e status.

O design foi limpo e moderno, com visual escuro, cores contrastantes e elementos que destacam os KPIs principais. A navegação ficou fluida e intuitiva.

---

## 🛠️ Aplicação de Conceitos de Engenharia de Dados

Além das análises e visualizações, este projeto também incorporou etapas comuns da **Engenharia de Dados**, como:

- **Automação da limpeza de dados**: o processo identifica e trata valores inválidos ou inconsistentes automaticamente.
- **Padronização dos dados**: remoção de erros de digitação, formatação e preenchimento adequado de campos nulos.
- **Armazenamento estruturado em banco de dados relacional (MySQL)**: os dados limpos foram inseridos em uma tabela dedicada, permitindo fácil reutilização, consultas otimizadas e integração com ferramentas de análise como Power BI e Python.

Essas práticas simulam um fluxo real de trabalho na área de dados, contribuindo para a construção de uma base sólida para projetos maiores e mais complexos no futuro.


## 🧠 Conclusão

Este projeto mostra na prática como criar um pipeline de análise de dados: da automação e limpeza até a visualização e extração de insights. Além de demonstrar domínio técnico em Python, SQL, Power BI e automações com banco de dados, ele prova como dados bem tratados geram análises confiáveis e decisões mais estratégicas.

