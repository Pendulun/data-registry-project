# Imagem base
FROM python:3.13

# Indica onde ficarão os arquivos copiados dentro do container
WORKDIR /app

# Instala o uv
RUN pip install uv

# Copia apenas os requirements para utilizar do caching do docker
COPY pyproject.toml uv.lock ./

# Instala os requirements
RUN uv sync --frozen

# Copia o resto da aplicação para dentro.
# Essa será a parte que mais vai invalidar o cache do build
COPY . .

# Expõe a porta 8000 interna para conexões externas
EXPOSE 8000

# Roda a aplicação fastapi em modo de execução (não em dev como no makefile)
CMD ["uv", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]