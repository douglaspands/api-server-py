import os
import re
import sys
import shutil
from time import sleep
from typing import Any, Dict, List, Tuple, Union, Optional

import toml
import yaml

cache = {}


# ===================================================
# SUPPORT FUNCTIONS
# ===================================================


def import_pyproject() -> Dict[str, Any]:
    global cache
    if not cache.get("pyproject"):
        with open("pyproject.toml", "r") as file_input:
            cache["pyproject"] = toml.loads(file_input.read())
    return cache["pyproject"]


def import_dockercompose() -> Dict[str, Any]:
    global cache
    if not cache.get("docker-compose"):
        with open("docker-compose.yaml", "r") as file_input:
            cache["docker-compose"] = yaml.load(file_input.read(), Loader=yaml.FullLoader)
    return cache["docker-compose"]


def get_app_basename() -> str:
    pyproject = import_pyproject()
    return pyproject["tool"]["poetry"]["name"]


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


def shell_run(command: Union[str, List[str]]) -> bool:
    res = True
    for cmd in command if isinstance(command, list) else [command]:
        print(f"$ {cmd}")
        if os.system(cmd):
            res = False
            break
    return res


# ===================================================
# POETRY SCRIPTS
# ===================================================


def deps():
    cmd = "docker-compose up -d apiserver-postgres apiserver-pgbouncer"
    shell_run(cmd)
    sleep(2)


def generate_badge_coverage():
    cmd = "coverage-badge -f -o docs/badge_coverage.svg"
    os.system(cmd)


def runserver():
    deps()
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    cmd = f"uvicorn --factory app.api:create_app --port {port} --reload"
    shell_run(cmd)


def lint(only_cmd: bool = False) -> Optional[List[str]]:
    app_basename = get_app_basename()
    cmd = [f"pflake8 {app_basename}", f"mypy {app_basename}", f"interrogate {app_basename}"]
    if not only_cmd:
        return shell_run(cmd)
    return cmd


def fiximports():
    app_basename = get_app_basename()
    cmd = f"isort {app_basename}"
    shell_run(cmd)


def codeformatter():
    app_basename = get_app_basename()
    cmd = f"black {app_basename}"
    shell_run(cmd)


def test(only_cmd: bool = False) -> Optional[List[str]]:
    cmd = ["PYTHONDONTWRITEBYTECODE=1 pytest -vvs"]
    if not only_cmd:
        if shell_run(cmd):
            generate_badge_coverage()
        return
    return cmd


def build():
    cmd = lint(True) + test(True)
    if shell_run(cmd):
        generate_badge_coverage()


def makemigrations():
    deps()
    cmd = "alembic revision --autogenerate"
    message = sys.argv[1] if len(sys.argv) > 1 else ""
    if not message:
        raise Exception("Required message about the change!")
    cmd = cmd + f' -m "{message}"'
    shell_run(cmd)


def migrate():
    deps()
    version = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    if version < 0:
        cmd = f"alembic downgrade {str(version)}"
    elif version > 0:
        cmd = f"alembic upgrade +{str(version)}"
    else:
        cmd = "alembic upgrade head"
    shell_run(cmd)


def requirements(only_cmd: bool = False) -> Optional[List[str]]:
    cmd = "poetry export -f requirements.txt --without-hashes --output requirements.txt"
    if not only_cmd:
        shell_run(cmd)
        return
    return cmd


def dbshell():
    deps()
    data = import_dockercompose()
    dbenv = data["services"]["apiserver-pgbouncer"]["environment"]
    dbenv["DB_HOST"] = "localhost"
    dbenv["DB_PORT"] = data["services"]["apiserver-pgbouncer"]["ports"][0].split(":")[0]
    cmd = (f"pgcli postgres://{dbenv['DB_USER']}:{dbenv['DB_PASSWORD']}@"
           f"{dbenv['DB_HOST']}:{dbenv['DB_PORT']}/{dbenv['DB_NAME']}")
    shell_run(cmd)


def dockerbuild():
    cmd = [requirements(True), "docker-compose build"]
    shell_run(cmd)


def pycacheremove():
    regex_success = re.compile(r"^.+[\/]__pycache__$")
    regex_deny = re.compile(r"(\.venv)|(scripts)")
    dirs, files = list_all_dirs_files()
    count = 0
    for d in dirs:
        if not regex_deny.search(d) and regex_success.search(d):
            try:
                shutil.rmtree(d)
                print(f"{d}:", "removed")
                count += 1
            except Exception as err:
                print(f"{d}:", str(err))
    print(f"{count} '__pycache__' folders have been removed!")


def cmd_test():
    """Command for tests"""
    data = import_dockercompose()
    dbenv = data["services"]["apiserver-pgbouncer"]["environment"]
    dbenv["DB_HOST"] = "localhost"
    dbenv["DB_PORT"] = data["services"]["apiserver-pgbouncer"]["ports"][0].split(":")[0]
    print(dbenv)
