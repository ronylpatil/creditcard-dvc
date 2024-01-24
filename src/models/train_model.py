import pathlib 
import yaml
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from src.log_config import infologger
from dvclive import Live

infologger.info('Executing : train_model.py')
infologger.info('purpose: train the model')

def train_model(train_features, target, n_estimators, max_depth, seed) :
     try : 
          model = RandomForestClassifier(n_estimators = n_estimators, max_depth = max_depth, random_state = seed)
          infologger.info(f'training {type(model).__name__} model')
          model.fit(train_features, target)
          pred_train = model.predict(train_features)
          accuracy = metrics.accuracy_score(target, pred_train)    # training accuracy

          try : 
               with Live(resume = True) as live :
                    # log model parameters
                    live.log_param('n_estimator', n_estimators)
                    live.log_param('max_depth', max_depth)
                    live.log_param('random_state', seed)
                    # log training metrics
                    # make plot = False, (only useful in case of iteration, make it false here)
                    live.log_metric('training/accuracy', float("{:.2f}".format(accuracy)))
                    live.log_metric('training/precision', float("{:.2f}".format(metrics.\
                                                                                precision_score(target, pred_train, zero_division = 1))))
                    live.log_metric('training/recall', float("{:.2f}".format(metrics.recall_score(target, pred_train))))

               infologger.info('successfully logged parameters & metrics through dvclive')
          except Exception as ie : 
               infologger.info(f'failed to load dvclive, encountered error {ie}')
          return model
     except Exception as oe : 
          infologger.info(f'failed to load model, encountered error {oe}')
          
          
def save_model(model, output_path) : 
     # Save the trained model to the specified output path
     try : 
          joblib.dump(model, output_path + '/model.joblib')
          infologger.info(f'model saved successfully at loc {output_path}')
     except Exception as e : 
          infologger.info(f'failed to dump the model, encountered error {e}')

def main() :
     curr_dir = pathlib.Path(__file__)
     home_dir = curr_dir.parent.parent.parent
     params_file = home_dir.as_posix() + '/params.yaml' 
     params = yaml.safe_load(open(params_file))
  
     # input_file = sys.argv[1]
     data_path = home_dir.as_posix() + params['make_dataset']['processed_data']
     output_path = home_dir.as_posix() + params['train_model']['model_loc']
     pathlib.Path(output_path).mkdir(parents = True, exist_ok = True)

     TARGET = params['base']['target_col']
     train_features = pd.read_csv(data_path + '/train.csv')
     X = train_features.drop(TARGET, axis = 1)
     y = train_features[TARGET]

     trained_model = train_model(X, y, params['train_model']['n_estimators'], params['train_model']['max_depth'],
                                 params['train_model']['seed'])
     save_model(trained_model, output_path)


if __name__ == "__main__" :
     main()
