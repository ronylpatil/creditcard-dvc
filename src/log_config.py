"""
If not able to access parent dir file inside child dir(sub-module/sub-pack) then follow this:
"https://stackoverflow.com/questions/714063/importing-modules-from-parent-folder/50194143#50194143" 

Just create dir as package and install it in editable mode using "pip install -e ."
Editable model : changes you make to the source code are immediately reflected in the installed package without the need to reinstall it.
creditcard/     (root dir)
|-- src/     (parent dir)
|   |-- __init__.py
|   |-- log.py
|   |-- data/    (child dir)
|       |-- __init__.py
|       |-- main.py   (here I want to access log.py)
|-- setup.py (create it in root)
|-- __init__.py (create it so it will recognized as package)

Now goto terminal at credicard loc and hit "pip install -e ."
That's it.
"""

import logging
import pathlib
from datetime import datetime

infologger = logging.getLogger(__name__)
infologger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')

log_file = f'{datetime.now().strftime("%d%b%y-%H.%M.%S")}.log'

log_dir_path = (pathlib.Path(__file__).parent.parent.as_posix() + '/logs')
pathlib.Path(log_dir_path).mkdir(parents = True, exist_ok = True)

log_file_path = pathlib.Path(log_dir_path + f'/{log_file}')
file_handler = logging.FileHandler(log_file_path)
file_handler.setFormatter(formatter)

infologger.addHandler(file_handler)

if __name__ == "__main__" :
     logging.info('Testing log')   