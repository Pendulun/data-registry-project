# data-registry-project
Um Data Registry é um sistema que gerencia datasets de uma organização. Ele é formado por CRUDs sobre versões, arquivos e acessos além de prover metadados sobre tais datasets.

Esse é um projeto pessoal para aprendizado. Com ele, vou treinar:
1. Criar uma API usando de FastAPI
2. Containerizar o projeto usando Docker
3. CI/CD com GitHub Actions
4. Outros a serem definidos

O objetivo é fazer isso tudo do zero pelo menos uma vez para depois estar confortável em usar uma IA para gerar tudo isso no dia a dia.

STATUS: Em desenvolvimento

## Arquitetura

O sistema está sendo desenvolvido seguindo a Arquitetura Hexagonal. Ela permite uma boa divisão entre regras de negócio e entidades (domínio) de serviços e ferramentas externas.

O servidor da aplicação usa de FastAPI e o banco é o Postgres. Cada uma dessas partes do sistema é um container Docker separado.

## O que é necessário para rodar

1. `uv`
2. `make`
3. Docker
4. Se não for rodar usando containers do Docker, é necessário:
    1. Postgres instalado e um banco criado a partir do schema em `./database/db_schema.sql`
    2. Criar um ambiente virtual (recomendado) com `uv sync`

## Configurações

O projeto possui um arquivo base `./.env.demo` que deve ser copiado para `./.env` e completado com as informações necessárias. Por exemplo:

```./.env
POSTGRES_DB=data_registry
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=data-registry-db
POSTGRES_PORT=5432
```
## Rodando a aplicação
O sistema tem 3 modos de execução:

1. Local: Nesse caso, o banco deve ser montado usando o schema disponibilizado em `./database/db_schema.sql` e o Postgres deve estar rodando na máquina local. Além disso, um ambiente com os requirements definidos em `pyproject.toml` deve estar disponível. É possível instalá-los com `uv sync` (é necessário ter o `uv` instalado na máquina).
2. Chamando os comandos Docker manualmente: Esse é o caso onde o Docker Compose não é usado. Para tal, é necessário chamar os seguintes comandos em ordem:
    1. `make create-network`
    2. `make run-db`
    3. `make run-app` ou `make run-app-dev` durante o desenvolvimento
3. Usando do Docker Compose: Para tal, basta chamar `make prd-up` (`make dev-up` durante o desenvolvimento). Para desligar, pode-se chamar `make down`.