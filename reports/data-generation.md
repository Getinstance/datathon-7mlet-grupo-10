# Relatório da geração de dados.

# Formatar isso depois.

## Cluster de Contexto
"Os segmentos de contexto não foram criados por regras manuais, mas sim utilizando o algoritmo K-Means sobre as variáveis X e Y. Encontramos K personas principais que foram mapeadas para a coluna context_segment."


## Vinculo de entidades
Vínculo de Entidades (Entity Linkage): > Como a base original do Kaggle não possui um identificador de usuário , optamos por criar uma Chave Artificial chamada profile_id durante a Etapa 1. Cada profile_id mapeia diretamente para uma linha de atributos demográficos e financeiros na base data/processed/. Os eventos registrados em offer_events.csv utilizam essa chave para permitir que o algoritmo contextual recupere os atributos (features) do cliente no momento da tomada de decisão da oferta.