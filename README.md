# API SERVER PY -- EM DESENVOLVIMENTO
Servidor de API REST desenvolvido em FastAPI/Python.

## IMAGEM DOCKER
Gerar imagem da aplicação:
```bash
docker-compose build fastapi
```
ou gerar a imagem e iniciar:
```bash
docker-compose up -d --build
```
Na imagem contem a aplicação e a ferramenta [Alembic](https://alembic.sqlalchemy.org/en/latest/) para execução dos scripts de migrate.   
Para executar o script de migrate no banco de dados é necessario 2 passos:
1. Acessar o container da aplicação:
```bash
docker exec -it apiserver-fastapi sh
```
2. Executar `Alembic` dentro do container para atualizar o banco de dados:
```sh
alembic upgrade head
```
> Para mais informações sobre o [Alembic](https://alembic.sqlalchemy.org/en/latest/), acessar a documentação.

## DESENVOLVIMENTO
Foi usado a versão `3.9.5` do Python.

### DOCKER E DOCKER-COMPOSE
A instalação varia de acordo com o sistema operacional, então aconselho verificar no site do [Docker](https://docs.docker.com/).

### LINUX/UBUNTU
Minha preferencia é desenvolver a aplicação no `Linux/Ubuntu` ou no `WSL2/Ubuntu`.
Para isso é necessario a instalação de algumas dependencias no Ubuntu:

- Pacotes essenciais para compilação:
```bash
sudo apt install build build-essential
```
- Lib para utilização do PostgreSQL:
```bash
sudo apt install build libpq-dev
```
- [Poetry](https://python-poetry.org/)
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
```
- [Pyenv](https://github.com/pyenv/pyenv)
```bash
sudo apt install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev && \
curl https://pyenv.run | bash
```

### POETRY - AUTOMATIZAÇÕES
Segue abaixo comandos para facilitar o desenvolvimento e a utilização de ferramentas:

- `poetry install` : **(Somente na primeira vez)** vai instalar todas as dependencias (inclusive de desenvolvimento);
- `poetry run runserver` : Iniciar a aplicação;
- `poetry run migrate` : Executa as migrations disponiveis;
- `poetry run makemigrations` : Cria migrations de acordo com as models da aplicação;
- `poetry run requirements` : Constroi o arquivo de `requirements.txt` para utilização no `Dockerfile`;
- `poetry run dbshell` : Abre a ferramenta `pgcli` conectada no banco de dados local;

> Comandos inspirados no framework Django. Porem no container não estarão disponiveis, aconselho olhar o arquivo `scripts.py` onde estão os comandos reais.

