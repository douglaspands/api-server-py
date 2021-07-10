import os
import re
import sys
import shutil
import platform
from typing import Any, Dict, List, Tuple, Union

import toml

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


def get_app_basename() -> str:
    pyproject = import_pyproject()
    return pyproject['tool']['poetry']['name']


def get_app_path() -> str:
    app_path = os.path.join(os.getcwd(), get_app_basename())
    return app_path


def list_all_dirs_files() -> Tuple[List[str], List[str]]:
    listdirs = []
    listfiles = []
    for root, subdirs, files in os.walk(get_app_path()):
        listfiles += [os.path.join(root, f) for f in files]
        listdirs += [os.path.join(root, s) for s in subdirs]
    return listdirs, listfiles


def shell_run(command: Union[str, List[str]]):
    and_ = ' & ' if platform.system() == 'Windows' else ' && '
    folder = f'cd {get_app_path()}'
    cmd_req = and_.join(command if isinstance(command, list) else [command])
    folder_cmd_req = folder + and_ + cmd_req
    print(cmd_req)
    os.system(folder_cmd_req)


# ===================================================
# POETRY SCRIPTS
# ===================================================

def deps():
    cmd = 'docker-compose up -d postgres'
    os.system(cmd)


def runserver():
    deps()
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    cmd = f'uvicorn --factory main:create_app --port {port} --reload'
    shell_run(cmd)


def test():
    cmd = f'pytest --cov={get_app_basename()} tests/'
    shell_run(cmd)


def lint():
    cmd = ['flake8 .']
    shell_run(cmd)


def makemigrations():
    deps()
    cmd = 'alembic revision --autogenerate'
    message = sys.argv[1] if len(sys.argv) > 1 else ''
    if message:
        cmd = cmd + f' -m "{message}"'
    shell_run(cmd)


def migrate():
    deps()
    cmd = 'alembic upgrade head'
    shell_run(cmd)


def requirements():
    cmd = 'poetry export -f requirements.txt --without-hashes --output requirements.txt'
    os.system(cmd)


def dbshell():
    deps()
    cmd = f'pgcli postgres://postgres:docker@localhost:5432/apiserver'
    os.system(cmd)


def pycacheremove():
    REGEX_DIR = re.compile(r'^.+[\/]__pycache__$')
    dirs, files = list_all_dirs_files()
    count = 0
    for d in dirs:
        if REGEX_DIR.search(d):
            shutil.rmtree(d)
            count += 1
    print(f'{count} folders have been removed')


def migrateremove():
    REGEX_DB = re.compile(r'^.+db\.sqlite3$')
    REGEX_FILE = re.compile(r'^.*[\/]migrations[\/].*$')
    REGEX_INITIAL = re.compile(r'^.*[\/]migrations[\/]__init__\.py$')
    dirs, files = list_all_dirs_files()
    count = 0
    for f in files:
        if (REGEX_FILE.search(f) and not REGEX_INITIAL.search(f)) or REGEX_DB.search(f):
            os.remove(f)
            count += 1
    print(f'{count} files have been removed')


def script_test():
    os.system('pwd')
