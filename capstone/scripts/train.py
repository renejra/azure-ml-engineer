from sklearn.linear_model import LogisticRegression
import argparse
import joblib
from sklearn.model_selection import train_test_split
from azureml.core import Workspace, Dataset, Run
import os
# from pathlib import Path


def clean_data(dataset):
    x = dataset.to_pandas_dataframe()
    x = x.dropna()
    dates = x.pop("Date")
    y = x.pop("y_c_shift")
    return x, y

def main():
    # Get workspace details
    run = Run.get_context()
    ws = run.experiment.workspace
    # ws = Workspace.from_config()
    # datastore = ws.get_default_datastore()

    # Parse hyperparameter as arguments for training script
    parser = argparse.ArgumentParser()
    parser.add_argument('--C', type=float, default=1.0,
                        help="Inverse of regularization strength. Smaller values cause stronger regularization")
    parser.add_argument('--max_iter', type=int, default=100, help="Maximum number of iterations to converge")
    parser.add_argument("--ds_name", type=str, default='hd-dataset')
    args = parser.parse_args()

    # clean the data
    dataset = Dataset.get_by_name(workspace=ws, name=args.ds_name)
    x, y = clean_data(dataset)
    x_train, x_test, y_train, y_test = train_test_split(x, y, shuffle=True, train_size=0.75)
    print(f'training shape: {x_train.shape}, labels: {y_train.shape} \ntesting shape: {x_test.shape}, labels: {y_test.shape}')
    print(x_train.tail(3))
    print(y_train.tail(3))

    # run logs
    run.log("regularization strength:", float(args.C))
    run.log("max iterations:", int(args.max_iter))

    # define model and pass in arguments
    model = LogisticRegression(C=args.C, max_iter=args.max_iter).fit(x_train, y_train)

    # evaluate after a run
    accuracy = model.score(x_test, y_test)
    run.log("accuracy", float(accuracy))

    # saving model
    os.makedirs('outputs', exist_ok=True)
    joblib.dump(value=model, filename='outputs/model-hd.joblib')

if __name__ == '__main__':
    main()