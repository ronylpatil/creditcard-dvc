# it will load data from drive and store in data/raw folder

import pathlib
import yaml
import pandas as pd
from sklearn.model_selection import train_test_split
from src.log_config import infologger   

infologger.info('Executing : load_dataset.py')
infologger.info('fetch data from google drive and store it in data/raw dir')

def load_data(remote_loc) :
    # Load your dataset from a given path
     try : 
          infologger.info(f'data source {remote_loc}')
          remote_loc = 'https://drive.google.com/uc?id=' + remote_loc.split('/')[-2]
          df = pd.read_csv(remote_loc)
          return df
     except Exception as e : 
          infologger.info(f'Loading data from remote location failed with error : {e}')
          return ''

def save_data(raw_data, output_path, file_name) : 
     # store data in data/raw dir
     try : 
          raw_data.to_csv(output_path + f'/{file_name}.csv', index = False)
          infologger.info(f'raw data saved suuccessfully at {output_path}')
     except Exception as e :
          infologger.info(f'Not able to save data. Error {e} caught.')

def main() : 
     curr_dir = pathlib.Path(__file__)    # at load_dataset.py
     home_dir = curr_dir.parent.parent.parent    # at creditcard_dvc
     param_file = home_dir.as_posix() + '/params.yaml'    # read from home dir
     params = yaml.safe_load(open(param_file))

     # input_file = sys.argv[1]
     remote_loc = params['data_source']['drive']
     output_path = home_dir.as_posix() + params['load_dataset']['raw_data']
     pathlib.Path(output_path).mkdir(parents = True, exist_ok = True)
     file_name = params['load_dataset']['file_name'] 

     data = load_data(remote_loc = remote_loc)
     save_data(data, output_path, file_name)

if __name__ == "__main__" : 
     main()
