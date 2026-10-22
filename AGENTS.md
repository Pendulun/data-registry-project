# AGENTS.md

## Comandos

- `uv sync` instala as dependências (Python 3.13, definido em `.python-version`).
- `make test` roda a suíte unitária completa; não precisa de banco nem de rede.
- Teste único: `uv run python -m unittest tests.unit.use_cases.test_create_dataset -v`
- Filtrar: `uv run python -m unittest discover -s tests -t . -k create_version -v`
- Rodar local: `make run-local` (exige `.env` e Postgres com `database/db_schema.sql` aplicado).
- Docker: `make prd-up` ou `make dev-up`; `make down` para encerrar.
- Não há lint, formatador nem typecheck configurados. Não invente esses comandos.
- O CI roda `uv sync --frozen`: ao mudar `pyproject.toml`, rode `uv add`/`uv lock` e commite `uv.lock`.

## Setup

- Copie `.env.demo` para `.env` (ignorado pelo git).
- `POSTGRES_HOST` deve ser `data-registry-db` dentro do Docker e `localhost` fora dele.
- `src/app/config/settings.py` lê o `.env` no import e monta o DSN; sem `.env`, o erro só aparece na primeira conexão.

## Arquitetura

- Hexagonal: `src/app/domain` (entidades), `src/app/ports/out` (ABCs), `src/app/use_cases`, `src/app/adapters/out` (Postgres, hasher, profiler) e `src/app/adapters/inward/api` (FastAPI). Entrypoint: `main.py:app`.
- Fluxo de uma feature: entidade → porta → caso de uso → adapter → router. Não há injeção de dependência: cada router cria `Database` e repositórios dentro do handler.
- Adapters de saída usam PascalCase (`DatasetRepoImp.py`, classe `DatasetRepoImp`) e são importados como `from src.app.adapters.out import DatasetRepoImp`, usando `DatasetRepoImp.DatasetRepoImp`. Siga esse padrão.
- Só `dataset`, `version`, `file` e `file_profile` estão implementados; as demais tabelas do schema são legado/planejado.

## Banco e SQL

- psycopg3 puro, sem ORM. Toda query em `src/app/adapters/out/*RepoImp.py` usa `%s` + tupla de parâmetros. Nunca interpole valores em f-string; os testes cobrem isso com `assert_parameterized`.
- IDs no banco são `bigint`, mas algumas entidades/portas ainda anotam `uuid.UUID` (`File.id`, `FileRepo.get_file_by_id`). Passe `int`; não confie na anotação.
- `database/db_schema.sql` é montado apenas na primeira inicialização do container Postgres. Mudou o schema? Recrie o volume ou aplique a alteração manualmente.
- `Database` abre uma conexão psycopg por request e não fecha (dívida conhecida). Não presuma pool.

## API e comportamento atual

- Sem tratamento de erros: casos de uso retornam `None` para duplicado/inexistente e a API responde 200 com corpo vazio; falhas de banco viram 500.
- Os testes de API cobrem apenas validação de entrada, que é o que falha antes do handler. Testar caminhos felizes exige Postgres ou patch dos repositórios no router.

## Testes

- `unittest` da stdlib; não há pytest. A descoberta exige `-t .` e os `tests/__init__.py` para os imports `src.app...`/`tests...` funcionarem.
- Sem banco nem rede: use `tests/fakes.py` (`FakeDatabase`, `FakeCursor`) e `tests/fixtures.py` (constantes e builders de linhas). Não repita literais nos testes.
- Nos repositórios, verifique a query parametrizada e a ordem dos parâmetros com `assert_parameterized`.
