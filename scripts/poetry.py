import os
import re
import sys
import shutil
import platform
from time import sleep
from typing import Any, Dict, List, Tuple, Union

import toml
import yaml

cache = {}


# ===================================================
# SUPPORT FUNCTIONS
# ===================================================

def import_pyproject() -> Dict[str, Any]:
    global cache
    if not cache.get('pyproject'):
        with open('pyproject.toml', 'r') as file_input:
            cache['pyproject'] = toml.loads(file_input.read())
    return cache['pyproject']


def import_dockercompose() -> Dict[str, Any]:
    global cache
    if not cache.get('docker-compose'):
        with open('docker-compose.yaml', 'r') as file_input:
            cache['docker-compose'] = yaml.load(file_input.read(), Loader=yaml.FullLoader)
    return cache['docker-compose']


def get_app_basename() -> str:
    pyproject = import_pyproject()
    return pyproject['tool']['poetry']['name']


def get_app_path() -> str:
    app_path = os.path.join(os.getcwd(), get_app_basename())
    return app_path


def list_all_dirs_files() -> Tuple[List[str], List[str]]:
    listdirs = []
    listfiles = []
    for root, subdirs, files in os.walk(os.getcwd()):
        listfiles += [os.path.join(root, f) for f in files]
        listdirs += [os.path.join(root, s) for s in subdirs]
    return listdirs, listfiles


def shell_run(command: Union[str, List[str]]):
    and_ = ' & ' if platform.system() == 'Windows' else ' && '
    join_cmd = and_.join(command if isinstance(command, list) else [command])
    print(join_cmd)
    os.system(join_cmd)


# ===================================================
# POETRY SCRIPTS
# ===================================================

def deps():
    cmd = 'docker-compose up -d apiserver-postgres apiserver-pgbouncer'
    shell_run(cmd)
    sleep(2)


def runserver():
    deps()
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    cmd = f'uvicorn --factory apiserver.main:create_app --port {port} --reload'
    shell_run(cmd)


def test():
    cmd = f'pytest --cov=./{get_app_basename()} tests/'
    shell_run(cmd)


def lint():
    cmd = ['flake8 .']
    shell_run(cmd)


def makemigrations():
    deps()
    cmd = 'alembic revision --autogenerate'
    message = sys.argv[1] if len(sys.argv) > 1 else ''
    if not message:
        raise Exception('Required message about the change!')
    cmd = cmd + f' -m "{message}"'
    shell_run(cmd)


def migrate():
    deps()
    cmd = 'alembic upgrade head'
    shell_run(cmd)


def requirements():
    cmd = 'poetry export -f requirements.txt --without-hashes --output requirements.txt'
    shell_run(cmd)


def dbshell():
    deps()
    data = import_dockercompose()
    dbenv = data['services']['apiserver-pgbouncer']['environment']
    dbenv['DB_HOST'] = 'localhost'
    dbenv['DB_PORT'] = data['services']['apiserver-pgbouncer']['ports'][0].split(':')[0]
    cmd = f"pgcli postgres://{dbenv['DB_USER']}:{dbenv['DB_PASSWORD']}@{dbenv['DB_HOST']}:{dbenv['DB_PORT']}/{dbenv['DB_NAME']}"
    shell_run(cmd)


def pycacheremove():
    REGEX_DIR = re.compile(r'^.+[\/]__pycache__$')
    dirs, files = list_all_dirs_files()
    count = 0
    for d in dirs:
        if REGEX_DIR.search(d):
            shutil.rmtree(d)
            count += 1
    print(f'{count} folders have been removed')


def cmd_test():
    """Command for tests
    """
    data = import_dockercompose()
    dbenv = data['services']['apiserver-pgbouncer']['environment']
    dbenv['DB_HOST'] = 'localhost'
    dbenv['DB_PORT'] = data['services']['apiserver-pgbouncer']['ports'][0].split(':')[0]
    print(dbenv)
