import os
import sys

import toml

with open('../pyproject.toml', 'r') as file_input:
    pyproject = toml.loads(file_input.read())

python_path = os.path.abspath(os.path.join(os.getcwd(), pyproject['tool']['poetry']['name']))

if python_path not in sys.path:
    sys.path.insert(0, python_path)
