run-local:
	uv run fastapi dev

# Cria a rede interna que vai ser usada pelos dois conteineres
# para que eles possam se comunicar
create-network:
	docker network create data-registry-network

# Inicia o container postgres que vai conter o banco
# Ele carrega o arquivo .env automaticamente e também
# cria o banco automaticamente a partir do db_schema.sql
run-db:
	docker run -d \
		--name data-registry-db \
		--network data-registry-network \
		--env-file .env \
		-v ./database/db_schema.sql:/docker-entrypoint-initdb.d/schema.sql \
		postgres:18

# Inicia o container do app que contém a aplicação.
# Acaba expondo a porta 8000 para que possamos chamar
# seus endpoints a partir do localhost. Está na mesma rede que
# o container do banco
run-app:
	docker build -f Dockerfile -t data-registry-app .
	docker run -d \
	-p 8000:8000 \
	--network data-registry-network \
	data-registry-app