# Animated Bassoon - Extrator de Dados do Jira

O Animated Bassoon é uma aplicação Python desenvolvida para extrair dados do Jira, permitindo que você obtenha informações de projetos, sprints e issues e as armazene no Elasticsearch para análise de produtividade das equipes via Kibana.

## Funcionalidades Principais

- Extrai dados de boards, sprints e issues (cards) do Jira
- Armazena os dados no Elasticsearch para análise e visualização
- Registra o histórico completo de mudanças de cada issue (status, board, sprint, assignee, etc.)

## Pré-requisitos

- Python instalado
- Docker e Docker Compose instalados

## Configuração

Crie um arquivo `.env` na raiz do projeto, utilizando como base o arquivo `env.config` com as seguintes variáveis de ambiente setadas:

```env
api_token=seu_token_jira ("https://id.atlassian.com/manage-profile/security/api-tokens")
email=seu_email_jira
domain=https://sua-empresa.atlassian.net

elastic_host=localhost
elastic_port=9200
```

## Uso

### Subindo a infraestrutura

Para subir o Elasticsearch e o Kibana:

```bash
docker compose up -d elasticsearch kibana
```

Aguarde o Elasticsearch estar saudável antes de rodar a aplicação:

```bash
curl http://localhost:9200
```

### Executando o extrator

```bash
make run
```

### Acessando o Kibana

Após a extração, acesse o Kibana em `http://localhost:5601` para visualizar os dados nos índices:

- `jira_issues` — issues com board e histórico de mudanças embutidos
- `jira_sprints` — sprints com métricas agregadas

### Queries no Kibana

> Dentro do diretório `docs/` há um documento com queries básicas para buscar dados específicos dos índices `jira_issues` e `jira_sprints`.

## Arquitetura

```
ExtractView  →  Elasticsearch  →  Kibana
                    
```

- **service/** — comunicação com a API do Jira
- **controller/** — orquestração da extração e paginação
- **infra/mappers/** — transformação dos dados do Jira para os models internos
- **infra/models/** — tipagem dos documentos (`Ticket`, `Sprint`, `ChangeHistory`)
- **infra/elastic_client.py** — comunicação com o Elasticsearch

## Histórico de Arquitetura

### Versão anterior

O projeto nasceu com uma arquitetura centrada em banco de dados relacional e métricas pré-calculadas.

O fluxo original funcionava assim:

```
Jira API  →  Extrator  →  SQLite/Postgres  →  Cálculo de métricas  →  S3 (AWS)
```

Os dados eram extraídos do Jira e persistidos em tabelas relacionais separadas — `board`, `sprint`, `issue` e `changelog` — usando SQLModel como ORM. Após a extração, a aplicação calculava automaticamente o **leadtime** e o **evolution leadtime**, gerava um gráfico e enviava a imagem para um bucket S3 na AWS.

Essa abordagem tinha limitações claras: as métricas eram fixas e definidas pelo código. Qualquer nova visualização ou corte diferente dos dados exigia uma alteração no código, um novo deploy e um novo envio para o S3. O usuário final não tinha controle sobre como queria ver os dados.

### Versão atual

A arquitetura foi refatorada para desacoplar a extração da visualização, dando autonomia total ao usuário para explorar os dados.

```
Jira API  →  Extrator  →  Elasticsearch  →  Kibana
```

Os dados agora são armazenados no Elasticsearch em dois índices desnormalizados — `jira_issues` e `jira_sprints` — com o histórico completo de mudanças de cada issue embutido no próprio documento. Isso elimina a necessidade de JOINs e torna cada documento autocontido.

O Kibana substitui o pipeline de métricas fixas e o S3. Em vez de receber imagens estáticas geradas pelo código, o usuário acessa um dashboard interativo onde pode criar suas próprias visualizações, filtrar por board, sprint, período, tipo de issue, responsável e qualquer outro campo disponível — sem precisar tocar no código.

Métricas como **leadtime**, **cycle time**, **velocity**, **throughput** e **CFD** passam a ser configuráveis diretamente no Kibana, adaptadas à realidade de cada time.

**A versão antiga estará disponível na branch `project/old-version` caso desejem vizualiza-la.**


## Estrutura dos documentos

### jira_issues

| Campo | Tipo | Descrição |
| --- | --- | --- |
| issue_id | int | ID do issue |
| key | str | Chave do issue (ex: PROJ-123) |
| status | str | Status atual |
| summary | str | Título do issue |
| issue_type | str | Tipo do issue |
| priority_name | str | Prioridade |
| board.id | int | ID do board |
| board.name | str | Nome do board |
| assignee.name | str | Nome do responsável |
| reporter.name | str | Nome do reporter |
| epic.key | str | Chave do épico |
| current_sprints | str | Sprint atual |
| belonged_sprint | str | Última sprint fechada |
| resolution_date | str | Data de resolução |
| creation_date | str | Data de criação |
| deleted | bool | Indica se o card foi deletado |
| changelog | array | Histórico de mudanças |
| changelog[].change_field | str | Campo alterado (status, board, sprint...) |
| changelog[].old_value | str | Valor anterior |
| changelog[].new_value | str | Novo valor |
| changelog[].change_timestamp | str | Data e hora da mudança |

### jira_sprints

| Campo | Tipo | Descrição |
| --- | --- | --- |
| sprint_id | int | ID da sprint |
| sprint_name | str | Nome da sprint |
| status | str | Status (active, closed, future) |
| origin_board | int | ID do board de origem |
| start_date | str | Data de início |
| end_date | str | Data de término |
| resolution_date | str | Data de conclusão |
| created_date | str | Data de criação |

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para enviar pull requests e reportar problemas.

## Licença

Este projeto é licenciado sob a MIT License.