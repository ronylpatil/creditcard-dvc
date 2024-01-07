import logging
import pathlib
from datetime import datetime

infologger = logging.getLogger(__name__)
infologger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')

log_file = f'{datetime.now().strftime("%d%b%y-%H.%M.%S")}.log'

log_dir_path = (pathlib.Path(__file__).parent.as_posix() + '/logs')
pathlib.Path(log_dir_path).mkdir(parents = True, exist_ok = True)

log_file_path = pathlib.Path(log_dir_path + f'/{log_file}')
file_handler = logging.FileHandler(log_file_path)
file_handler.setFormatter(formatter)

infologger.addHandler(file_handler)

if __name__ == '__main__' :
     logging.info('Testing log.')