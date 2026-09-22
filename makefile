# Versão para rodar o app localmente sem container. O banco deve estar no host
run-local:
	uv run fastapi dev

# Versões usando o Dockerfile e chamada manual ao Docker

# Cria a rede interna que vai ser usada pelos dois conteineres
# para que eles possam se comunicar
create-network:
	docker network inspect data-registry-network >/dev/null 2>&1 || \
	docker network create data-registry-network

# Inicia o container postgres que vai conter o banco
# Ele carrega o arquivo .env automaticamente e também
# cria o banco automaticamente a partir do db_schema.sql.
# Faz o bind-mount do schema do banco. 
# Cria um volume para persisteir os dados do banco
run-db: create-network
	docker run -d \
		--name data-registry-db \
		--network data-registry-network \
		--env-file .env \
		-v ./database/db_schema.sql:/docker-entrypoint-initdb.d/schema.sql \
		-v data-registry-db-data:/var/lib/postgresql \
		postgres:18

# Inicia o container do app que contém a aplicação.
# Acaba expondo a porta 8000 para que possamos chamar
# seus endpoints a partir do localhost. Está na mesma rede que
# o container do banco
run-app: create-network
	docker build -f Dockerfile -t data-registry-app .
	docker run -d \
		-p 8000:8000 \
		--network data-registry-network \
		--env-file .env \
		data-registry-app

# Versão de desenvolvimento. Usa bind-mount para que alterações
# no host reflitam no container facilitando o desenvolvimento
run-app-dev: create-network
	docker build -f Dockerfile -t data-registry-app .
	docker run -d \
		--name data-registry-app \
		-p 8000:8000 \
		--network data-registry-network \
		-v .:/app \
		-v data-registry-app-venv:/app/.venv \
		--env-file .env \
		data-registry-app \
		python -m fastapi dev main.py --host 0.0.0.0 --port 8000

# Versões usando o Docker compose
dev-up:
	docker compose -f compose.yaml -f compose.dev.yaml up
	
prd-up:
	docker compose up

down:
	docker compose down