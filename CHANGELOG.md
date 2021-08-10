# Changelog
Todas as notas de alteração deste projeto vão ser documentadas neste arquivo.

O formato é baseado no [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere o [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]
- Construção do motor de testes orientado a comportamento (BDD/Behave);
- Construção do motor de processamento de tarefas assincronas (Celery);
- Construção do motor de processamento de tarefas agendadas (Celery Beat);
- Criação e configuração de escopos do token OAUTH2;

## [0.3.0] - 2021-08-10
### Added
- Foi adicionado o framework de formatação `black` para formatação de código;
- Inclusão do arquivo `CHANGELOG.md`;

### Changed
- Foi instalado o wrapper `pflake8` para facilitar a movimentação das configurações do `flake8` que estão no `setup.cfg` para o `pyproject.toml`;
- Foi movimentado todas as configurações do arquivo `setup.cfg` para o `pyproject.toml`;
