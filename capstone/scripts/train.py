from sklearn.linear_model import LogisticRegression
import argparse
import os
# import numpy as np
# from sklearn.metrics import mean_squared_error
import joblib
from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from azureml.core import Workspace
from azureml.core.run import Run
from azureml.data.dataset_factory import TabularDatasetFactory
# import requests
# import io

# Connect to workspace
ws = Workspace.from_config()
datastore = ws.get_default_datastore()

dataset = get(ws, name='hd-dataset')

def clean_data(data):
    y_df = x_df.pop("y_c_shift")
    return x_df, y_df

# Clean data and split for training and testing
x, y = clean_data(dataset)
x_train, x_test, y_train, y_test = train_test_split(x, y, shuffle=True, train_size=0.75)
print(f'training shape: {x_train.shape}, labels: {y_train.shape} \ntesting shape: {x_test.shape}, labels: {y_test.shape}')

run = Run.get_context()

def main():
    # Add arguments to script
    parser = argparse.ArgumentParser()

    parser.add_argument('--C', type=float, default=1.0,
                        help="Inverse of regularization strength. Smaller values cause stronger regularization")
    parser.add_argument('--max_iter', type=int, default=100, help="Maximum number of iterations to converge")

    args = parser.parse_args()

    run.log("regularization strength:", float(args.C))
    run.log("max iterations:", int(args.max_iter))

    model = LogisticRegression(C=args.C, max_iter=args.max_iter).fit(x_train, y_train)

    accuracy = model.score(x_test, y_test)
    run.log("accuracy", float(accuracy))

    # Saving model
    joblib.dump(model,"./outputs/model-hd.joblib")

if __name__ == '__main__':
    main()