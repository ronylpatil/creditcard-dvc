import yaml
import joblib
import pathlib
import pandas as pd
from dvclive import Live
from sklearn import metrics
from src.log_config import infologger

infologger.info('Executing : predict_model.py')
infologger.info('purpose: evaluate the model and log the data')


def load_model(model_path) : 
     # load model and return it
     try : 
          with open(model_path + '/model.joblib', 'rb') as f :
               model = joblib.load(f)
          return model
     except Exception as e : 
          infologger.info(f'failed to load model, encountered error {e}')


def evaluate(data, model_path) :
     try : 
          model = load_model(model_path = model_path)
          infologger.info(f'model loaded successfully from path: {model_path}')
     except Exception as e : 
          infologger.info(f'failed to load model, encountered error {e}')
     else : 
          TARGET = [params['base']['target_col']]
          X = data.drop(TARGET, axis = 1)
          y = data[TARGET]

          predictions_by_class = model.predict_proba(X)
          y_pred = model.predict(X)
          predictions = predictions_by_class[:, 1]
          try : 
          # track all using live
               with Live(resume = True) as live :
                    live.log_metric('testing/roc_auc_score', float("{:.2f}".format(metrics.roc_auc_score(y, predictions))))
                    live.log_metric('testing/bal_acc_score', float("{:.2f}".format(metrics.balanced_accuracy_score(y, y_pred))))
                    live.log_metric('testing/recall', float("{:.2f}".format(metrics.recall_score(y, y_pred))))
                    live.log_metric('testing/precision', float("{:.2f}".format(metrics.precision_score(y, y_pred, zero_division = 1))))
               
               infologger.info('testing metrics logged successfully')
          except Exception as e : 
               infologger.info(f'failed to log metrics, encountered error {e}')


if __name__ == '__main__' : 
     curr_dir = pathlib.Path(__file__)
     home_dir = curr_dir.parent.parent.parent
     params_file = home_dir.as_posix() + '/params.yaml' 
     params = yaml.safe_load(open(params_file))
     model_path = home_dir.as_posix() + params['train_model']['model_loc']

     # train_data = pd.read_csv(f"{home_dir.as_posix()}{params['make_dataset']['processed_data']}/train.csv")
     test_data = pd.read_csv(f"{home_dir.as_posix()}{params['make_dataset']['processed_data']}/test.csv")

     # Evaluate test datasets.
     evaluate(test_data, model_path)
