# API SERVER PY -- EM DESENVOLVIMENTO
Servidor de API REST desenvolvido em FastAPI/Python.

## INICIAR A APLICAÇÃO

Vamos iniciar a aplicação com o Docker e Docker Compose, vamos executar o seguinte comando:
```bash
docker-compose up -d
```
Acessar a documentação da aplicação pelas urls:
- [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
- [http://localhost:8000/api/redoc](http://localhost:8000/api/redoc)

Algumas observações:
- Na imagem contem a ferramenta [Alembic](https://alembic.sqlalchemy.org/en/latest/) para execução dos scripts de migrate;
- A imagem da aplicação é preparada para o desenvolvimento, caso altere algum arquivo é reiniciado automaticamente;
- Da para acompanhar as querys executadas no PostgreSQL executando o comando: `docker logs --follow --tail=1 apiserver-postgres`

## DESENVOLVIMENTO
Foi usado a versão `3.8` do Python.

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

