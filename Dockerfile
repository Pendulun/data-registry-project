# 1. Passo builder: Cria um ambiente virtual e instala as dependências
# Imagem base
FROM python:3.13-slim AS builder

# Indica onde ficarão os arquivos copiados dentro do container
WORKDIR /app

# Necessário para instalar o psycopg
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instala o uv
RUN pip install uv

# Copia apenas os requirements para utilizar do caching do docker
COPY pyproject.toml uv.lock ./

# Instala os requirements
RUN uv sync --frozen

# 2. Passo final: Utiliza do ambiente virtual criado no builder
# não precisa do uv ou das libs para compilar o psycopg
FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/.venv /app/.venv
# Copia o resto da aplicação para dentro.
# Essa será a parte que mais vai invalidar o cache do build
COPY . .

# Expõe a porta 8000 interna para conexões externas
EXPOSE 8000

# Roda a aplicação fastapi em modo de execução (não em dev como no makefile)
CMD ["/app/.venv/bin/fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]