# Dicionário de dados:

##  Dados do Cliente:

| Campo | Descrição | Tipo / Valores |
|---|---|---|
| age | Idade do cliente | numérico |
| job | Tipo de emprego | categórico: 'admin.', 'blue-collar', 'entrepreneur', 'housemaid', 'management', 'retired', 'self-employed', 'services', 'student', 'technician', 'unemployed', 'unknown' |
| marital | Estado Civil | categórico: 'divorced', 'married', 'single', 'unknown' (note: 'divorced' significa divorciado ou viúvo) |
| education | Educação | categórico: 'basic.4y', 'basic.6y', 'basic.9y', 'high.school', 'illiterate', 'professional.course', 'university.degree', 'unknown' |
| default | Possui crédito em inadimplência? | categórico: 'no', 'yes', 'unknown' |
| housing | Possui empréstimo habitacional? | categórico: 'no', 'yes', 'unknown' |
| loan | Possui empréstimo pessoal? | categórico: 'no', 'yes', 'unknown' |

##  Dados do último contato:

| Campo | Descrição | Tipo / Valores |
|---|---|---|
| Month | Mês do último contato | categórico: 'jan', 'feb', 'mar', ..., 'nov', 'dec' |
| Day_of_week | Dia da semana do último contato | categórico: 'mon', 'tue', 'wed', 'thu', 'fri' |

##  Dados socioeconômicos

| Campo | Descrição | Tipo |
|---|---|---|
| Emp.var.rate | Taxa de variação do emprego | Trimestral, numérico |
| Cons.price.idx | Índice de preços ao consumidor | Mensal, numérico |
| Cons.conf.idx | Índice de confiança do consumidor | Mensal, numérico |
| Euribor3m | Taxa Euribor de 3 meses | Diário, numérico |
| Nr.employed | Número de empregados | Trimestral, numérico |
| cluster | Rótulo de cluster do KMeans aplicado às características pessoais | categórico |

##  Variavel de saída (alvo):

| Campo | Descrição | Tipo / Valores |
|---|---|---|
| y | Cliente aderiu ao depósito a prazo? | binário: 'yes', 'no' |