# Changelog
Todas as notas de alteração deste projeto vão ser documentadas neste arquivo.

O formato é baseado no [Mantenha um Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere o [Versionamento Semântico](https://semver.org/lang/pt-BR/).


## [Não publicado]

### Adicionado
- Construção do motor de testes orientado a comportamento (BDD/Behave);
- BDD Feature do dominio de usuarios;

## [0.3.1] - 2021-08-10
### Adicionado
- Script `poetry run dockerbuild` para geração do requirements.txt e imagem docker da aplicação;

### Modificado
- `CHANGELOG.md` em português;

## [0.3.0] - 2021-08-10
### Adicionado
- Foi adicionado o framework de formatação `black` para formatação de código;
- Inclusão do arquivo `CHANGELOG.md`;

### Modificado
- Foi instalado o wrapper `pflake8` para facilitar a movimentação das configurações do `flake8` que estão no `setup.cfg` para o `pyproject.toml`;
- Foi movimentado todas as configurações do arquivo `setup.cfg` para o `pyproject.toml`;
