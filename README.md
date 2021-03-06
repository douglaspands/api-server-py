# API SERVER PY
<p>
<a href="https://interrogate.readthedocs.io/en/latest/"><img src="./docs/badge_interrogate.svg"></a>
<a href="https://pytest-cov.readthedocs.io/en/latest/readme.html"><img src="./docs/badge_coverage.svg"></a>
</p>

Servidor de API REST desenvolvido em Python e PostgreSQL utilizando: FastAPI, Gunicorn/Uvicorn, ORMAR, Alembic e Poetry.

### INICIAR A APLICAÇÃO
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

### METAS
- [x] Criar e configurar automações (Poetry);
- [x] Construção do CRUD de usuarios (FastAPI);
- [x] ORM assincrono (ORMAR);
- [x] Aplicando frameworks de boas praticas nas APIs (OpenBanking+Blueprint);
- [x] Construção do login simples e validação dele nas rotas (JWT);
- [x] Centralizar configurações da aplicação (Pydantic);
- [x] Configurar script de migrations e construir adaptador assincrono (Alembic+ORMAR);
- [x] Configurar servidores http e de aplicação (NginX+Gunicorn+Uvicorn);
- [x] Conteinerizar a aplicação (Docker+Docker-Compose);
- [x] Configurar aplicação e banco de dados para funcionar em modo de desenvolvimento;
- [x] Gerenciador de conexões com o Banco de Dados (PgBouncer);
- [x] Cliente de banco de dados para desenvolvimento (psql+pgcli);
- [x] Configurar e aplicar linters de qualidade de codigo (Flake8+Mypy+Interrogate)
- [x] Teste unitario e cobertura (Pytest+Coverage);
- [x] Unificando configurações do projeto (PEP-518);
- [ ] Testes orientado a comportamento (Behave);
- [ ] Processamento de tarefas assincronas (Celery);
- [ ] Processamento de tarefas agendadas (Celery Beat);
- [ ] Validação de escopo do token OAUTH2;

### DESENVOLVIMENTO
Foi usado o Python `3.8` para desenvolvimento. 
> Python 3.8 foi a escolha devido a melhor compatibilidade entre todas as ferramentas e dependencias utilizadas. Foi identificado algumas incompatibilidades com a versão 3.9, mas acredito que seja algo temporario.

#### DOCKER E DOCKER-COMPOSE
A instalação varia de acordo com o sistema operacional, então aconselho verificar no site do [Docker](https://docs.docker.com/).

#### LINUX/UBUNTU
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

#### POETRY - AUTOMATIZAÇÕES
Segue abaixo comandos para facilitar o desenvolvimento e a utilização de ferramentas:

- **poetry install** : (SOMENTE NA PRIMEIRA VEZ) Vai instalar todas as dependencias (inclusive de desenvolvimento). Antes de executar, eu construi o ambiente com o `Pyenv`:
```bash
pyenv install 3.8.10 && pyenv local 3.8.10
```
- **poetry run runserver** : Iniciar a aplicação;
- **poetry run migrate** : Executa as migrations disponiveis;
- **poetry run makemigrations** : Cria migrations de acordo com as models da aplicação;
- **poetry run requirements** : Constroi o arquivo de `requirements.txt` para utilização no `Dockerfile`;
- **poetry run dbshell** : Abre a ferramenta `pgcli` conectada no banco de dados local;
- **poetry run lint** : Verifica a qualidade do código;
- **poetry run test** : Executa os testes unitarios e a cobertura de testes gerando o relatorio no `htmlcov/index.html`;
- **poetry run build** : Executa os comandos `lint` e `test` na sequencia para verificação da qualidade do código e erros de teste;
- **poetry run fiximports**: Organiza e classifica os imports do projeto;
- **poetry run codeformatter**: Formata o código do projeto usando o `black`;
> Comandos inspirados no framework Django. Porem no container não estarão disponiveis, aconselho olhar o arquivo `scripts/poetry.py` onde estão os comandos reais.


###  FONTES
Fontes que ajudaram (ou ajudarão) no desenvolvimento desse projeto:

- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [ormar](https://github.com/collerek/ormar)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Pytest](https://docs.pytest.org/en/6.2.x/)
- [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio)
- [pytest-cov](https://github.com/pytest-dev/pytest-cov)
- [behave-restful](https://github.com/behave-restful/behave-restful)
- [behave-html-formatter](https://github.com/behave-contrib/behave-html-formatter)
- [Poetry](https://python-poetry.org/)
- [Pyenv](https://github.com/pyenv/pyenv)
- [Docker](https://docs.docker.com/)
- [uvicorn-gunicorn](https://github.com/tiangolo/uvicorn-gunicorn-docker)
- [pgcli](https://www.pgcli.com/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [PgBouncer](https://www.pgbouncer.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Nginx](https://hub.docker.com/_/nginx)
- [OpenBanking API Specifications](https://standards.openbanking.org.uk/api-specifications/)
- [Domain Driven Design](https://martinfowler.com/tags/domain%20driven%20design.html)
- [MailHog](https://github.com/mailhog/MailHog)
- [interrogate](https://interrogate.readthedocs.io/en/latest/)
- [Changelog](https://keepachangelog.com/en/1.1.0/)
- [PEP-8](https://www.python.org/dev/peps/pep-0008/)
- [PEP-257](https://www.python.org/dev/peps/pep-0257/)
- [PEP-518](https://www.python.org/dev/peps/pep-0518/)
