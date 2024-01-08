import pathlib
import yaml
import pandas as pd
from sklearn.model_selection import train_test_split
from src.log_config import infologger   

infologger.info('Executing : make_dataset.py')
infologger.info('purpose: fetch data from data/raw and perform train-test split')

def load_data(data_path) :
    # Load your dataset from a given path
    try : 
        infologger.info(f'data source {data_path}')
        data = pd.read_csv(data_path)
        infologger.info('data loaded successfully')
        return data
    except Exception as e : 
        infologger.info(f'encountered error {e} while loading data')
        return ''

def split_data(df, test_split, seed) :
    # Split the dataset into train and test sets
    try : 
        train, test = train_test_split(df, test_size = test_split, random_state = seed)
        infologger.info(f'perform train-test split with test_split = {test_split} and seed = {seed}')
        return train, test
    except Exception as e : 
        infologger.info(f'encountered error {e} while spliting data')
        return ''

def save_data(train, test, output_path) :
    # Save the split datasets to the specified output path
    try : 
        train.to_csv(output_path + '/train.csv', index = False)
        test.to_csv(output_path + '/test.csv', index = False)
        infologger.info(f'splited data saved suuccessfully at {output_path}')
    except Exception as e : 
        infologger.info(f'encountered error {e} while saving the splited data')

def main() :
    curr_dir = pathlib.Path(__file__)
    home_dir = curr_dir.parent.parent.parent
    param_file = home_dir.as_posix() + '/params.yaml'
    params = yaml.safe_load(open(param_file))

    # input_file = sys.argv[1]
    data_path = home_dir.as_posix() + params['load_dataset']['raw_data'] 
    output_path = home_dir.as_posix() + params['make_dataset']['processed_data']
    pathlib.Path(output_path).mkdir(parents = True, exist_ok = True)
    data_file = f"{data_path}/{params['load_dataset']['file_name']}.csv"

    data = load_data(data_path = data_file)
    train_data, test_data = split_data(data, params['make_dataset']['test_split'], params['make_dataset']['random_state'])
    save_data(train_data, test_data, output_path)

if __name__ == "__main__" :
    main()  
