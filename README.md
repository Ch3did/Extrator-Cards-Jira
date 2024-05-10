# Animated Bassoon - Extrator de Dados do Jira

O Animated Bassoon é uma aplicação Python desenvolvida para extrair dados do Jira, permitindo que você obtenha informações de projetos, sprints e issues diariamente e as armazene em um banco de dados para análise de produtividade das equipes.

## Funcionalidades Principais:
- Extrai dados de boards (projetos), sprints e issues (cards) do Jira.
- Armazena os dados em um banco de dados para análise posterior.
- Calcula leadtime e evolution leadtime a partir dos dados extraídos do Jira.
- Gera um gráfico representando o leadtime e evolution leadtime.
- Salva a imagem do gráfico no serviço de armazenamento S3.

## Pré-requisitos:
- Python instalado.
- Pip instalado.

## Configuração:

Durante a execução do código, um arquivo chamado .env será criado. Caso não seja alterado o nome da variável database_url neste arquivo, o nome do banco de dados será `"test_app.db"` e ele estará localizado no diretório `.tmp`.

## Instalação:

Para instalar o Animated Bassoon, execute o seguinte comando:

```
make install
```

## Uso:

Para executar o Animated Bassoon, utilize o seguinte comando:

```
make run
```

### Observações:

Certifique-se de configurar corretamente as credenciais do Jira no arquivo .env antes de executar a aplicação.


## Objetos criados e suas estruturas

### Board

| Nome do Campo        | Tipo de Dado         | Descrição                               |
|----------------------|----------------------|-----------------------------------------|
| id                   | int (Opcional)       | Chave primária da tabela                |
| board_id             | int                  | ID do board                             |
| board_name           | str                  | Nome do board                           |
| board_url            | str                  | URL do board                            |
| board_type           | str                  | Tipo do board                           |
| colected_time_stemp  | datetime (Opcional)  | Timestamp de coleta (com timezone)      |

### Changelog

| Nome do Campo        | Tipo de Dado         | Descrição                               |
|----------------------|----------------------|-----------------------------------------|
| id                   | int (Opcional)       | Chave primária da tabela                |
| issue_id             | int                  | ID do issue associado ao changelog      |
| change_id            | int                  | ID da mudança                           |
| creator              | str                  | Criador da mudança                      |
| change_date          | datetime             | Data da mudança                         |
| change_field         | str                  | Campo alterado                          |
| old_value            | str (Opcional)       | Valor antigo                            |
| new_value            | str (Opcional)       | Novo valor                              |
| colected_time_stemp  | datetime (Opcional)  | Timestamp de coleta (com timezone)      |

### Issue

| Nome do Campo               | Tipo de Dado         | Descrição                               |
|-----------------------------|----------------------|-----------------------------------------|
| id                          | int (Opcional)       | Chave primária da tabela                |
| issue_id                    | int                  | ID do issue                             |
| board_id                    | int                  | ID do board associado ao issue          |
| expand                      | str                  | Expandir                                |
| status                      | str                  | Status do issue                         |
| self_url                    | str                  | URL do issue                            |
| key                         | str                  | Chave do issue                          |
| issue_type                  | str                  | Tipo do issue                           |
| issue_type_id               | str                  | ID do tipo de issue                     |
| summary                     | str                  | Resumo do issue                         |
| priority_name               | str                  | Nome da prioridade                      |
| epic_id                     | int (Opcional)       | ID do épico associado ao issue          |
| epic_key                    | str (Opcional)       | Chave do épico associado ao issue       |
| epic_name                   | str (Opcional)       | Nome do épico associado ao issue        |
| epic_summary                | str (Opcional)       | Resumo do épico associado ao issue      |
| sprint                      | str (Opcional)       | Sprint associada ao issue               |
| work_ratio                  | int (Opcional)       | Razão de trabalho                       |
| reporter_name               | str (Opcional)       | Nome do reporter                        |
| reportar_mail               | str (Opcional)       | E-mail do reporter                      |
| creators_name               | str (Opcional)       | Nome do criador                         |
| creators_mail               | str (Opcional)       | E-mail do criador                       |
| progress                    | str (Opcional)       | Progresso                               |
| status_category_change_date | datetime (Opcional)  | Data da mudança de categoria de status  |
| timespent                   | datetime (Opcional)  | Tempo gasto                             |
| resolution_date             | datetime (Opcional)  | Data de resolução                       |
| creation_date               | datetime (Opcional)  | Data de criação                         |
| closed_sprint               | str (Opcional)       | Sprint fechada                          |
| colected_time_stemp         | datetime (Opcional)  | Timestamp de coleta (com timezone)      |

### Sprint

| Nome do Campo        | Tipo de Dado         | Descrição                               |
|----------------------|----------------------|-----------------------------------------|
| id                   | int (Opcional)       | Chave primária da tabela                |
| sprint_id            | int                  | ID da sprint                            |
| status               | str                  | Status da sprint                        |
| self_url             | str                  | URL da sprint                           |
| sprint_name          | str                  | Nome da sprint                          |
| origin_board         | int                  | Board de origem da sprint               |
| start_date           | datetime (Opcional)  | Data de início da sprint                |
| resolution_date      | datetime (Opcional)  | Data de resolução da sprint             |
| created_date         | datetime (Opcional)  | Data de criação da sprint               |
| end_date             | datetime (Opcional)  | Data de término da sprint               |
| colected_time_stemp  | datetime (Opcional)  | Timestamp de coleta (com timezone)      |



## Contribuição:

Contribuições são bem-vindas! Sinta-se à vontade para enviar pull requests e reportar problemas.

## Licença:

Este projeto é licenciado sob a MIT License.

Nota: Certifique-se de substituir os valores de database_url e test_app.db conforme necessário, de acordo com sua configuração.