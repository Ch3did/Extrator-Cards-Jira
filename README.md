# Animated Bassoon - Extrator de Dados do Jira

O Animated Bassoon é uma aplicação Python desenvolvida para extrair dados do Jira, permitindo que você obtenha informações de projetos, sprints e issues diariamente e as armazene em um banco de dados para análise de produtividade das equipes.

## Funcionalidades Principais:
- Extrai dados de boards (projetos), sprints e issues (cards) do Jira.
- Armazena os dados em um banco de dados para análise posterior.

## Pré-requisitos:
- Python instalado.
- Pip instalado.


## Configuração:

Durante a execução do código, um arquivo chamado .env será criado. Caso não seja alterado o nome da variável database_url neste arquivo, o nome do banco de dados será test_app.db e ele estará localizado no diretório .tmp.

## Instalação:

Para instalar o Animated Bassoon, execute o seguinte comando:

> make install

# Uso:

Para executar o Animated Bassoon, utilize o seguinte comando:

> make run

## Observações:

Certifique-se de configurar corretamente as credenciais do Jira no arquivo .env antes de executar a aplicação.

## Contribuição:

Contribuições são bem-vindas! Sinta-se à vontade para enviar pull requests e reportar problemas.

# Licença:

Este projeto é licenciado sob a MIT License.

Nota: Certifique-se de substituir os valores de database_url e test_app.db conforme necessário, de acordo com sua configuração.