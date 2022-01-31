# Using AzureML for Bitcoin trading signals

This is my capstone project for Udacity's ML Engineer in Azure nanodegree. In this project, I will use AzureML
capabilities to train, tune and deploy a machine learning powered trading signal, to predict whether on the next day,
Bitcoin prices would go up (BUY, 1), down (SELL, -1) or stay around the same (HOLD, 0).

## Project Set Up and Installation
In order to setup this project, you will need certain libraries installed. The easiest way to do this is to install
conda, and run the following line on a terminal within the `/casptone` directory:

```bash
conda install --file envs/env.yml
```
This will install all dependencies needed for this project, creating an environment named `az-capstone`. This file
is also used within AzureML, to download relevant dependencies into a reproducible environment, that we can use
to train, tune and deploy our models on the cloud platform with ease.

In order for the data sourcing and preprocessing part to work, you will additionally need to setup a Quandl account,
and input your Quandl Api Key as an environment variable.

```bash
export QUANDLKEY="your-quandl-api-secret"
```
For the notebooks to be able to connect to your relevant Azure subscription and ML Studio
instance, you will need to provide a `config.json` file in the following format:
```bash
{
  this: that
  this: that
  this: that
}
```
This file is loaded on the [automl notebook](2-automl.ipynb) and the [hyperdrive](3-hyperparameter_tuning.ipynb) one
to create a connection with your AzureML resources.

## Dataset

### Overview
The data I will be using include financial data (important stock indices, volume, interest rates, money supply...), 
Bitcoin fundamentals (transactions, transaction cost, hashrate...), commodity prices (gold, silver, oil), and 
relevant technical indicators that traders use (moving averages, Stochastic Relative Strenght Index,
standard deviation...). Financial data and commodities price were sourced from Yahoo Finance using `yfinance` library, 
fundamentals were sourced using `Quandl` and technical indicators were all self-developed. You will find the 
functions for these technical indicators on the `data_utils` folder.

On the [data sourcing notebook](1-data-sourcing.ipynb) you will find all the steps done to get and preprocess the data.
Running the notebook will create CSV files on the `data/` directory. These files are then registered on AzureML
in the relevant AutoML and HyperDrive notebooks, from which they are taken for training and tuning models.

### Task
The task I will be using the Dataset for, is a **classification** task. My aim is to use the data mentioned above
to predict on a day-ahead basis if the asset returns will be on the top 25% most positive returns (BUY, 1), 
the 25% most negative days (SELL, -1) or everything in between (HOLD, 0). While this project is focusing on Bitcoin
prices, this approach is generally extensible to any other asset class, as long as we have reasons to believe
that there is a certain relationship with the financial market.

It is important to note, that the datasets we will take for the next steps differ depending on their nature. 
Since by using AutoML all the data transformation, normalization and standarization is handled by Azure, 
we will feed in a non-treated copy of the dataset. 
On the other hand, as we need to tune in our parameters ourselves on HyperDrive experiment, we will also take care of
the data transformation, normalization and standarization steps, that should be important for the model to converge.

### Access
The access to the data is done on each notebook initially by reading the relevant CSV file on the `data/` directory,
but they are then registered on AzureML as a Dataset prior training. If you want to have a look into
how the data was sourced in detail, please check the [data sourcing notebook](1-data-sourcing.ipynb).

## Automated ML
*TODO*: Give an overview of the `automl` settings and configuration you used for this experiment

### Results
*TODO*: What are the results you got with your automated ML model? What were the parameters of the model? How could you have improved it?

*TODO* Remeber to provide screenshots of the `RunDetails` widget as well as a screenshot of the best model trained with it's parameters.

## Hyperparameter Tuning
*TODO*: What kind of model did you choose for this experiment and why? Give an overview of the types of parameters and their ranges used for the hyperparameter search


### Results
*TODO*: What are the results you got with your model? What were the parameters of the model? How could you have improved it?

*TODO* Remeber to provide screenshots of the `RunDetails` widget as well as a screenshot of the best model trained with it's parameters.

## Model Deployment
*TODO*: Give an overview of the deployed model and instructions on how to query the endpoint with a sample input.

## Screen Recording
*TODO* Provide a link to a screen recording of the project in action. Remember that the screencast should demonstrate:
- A working model
- Demo of the deployed  model
- Demo of a sample request sent to the endpoint and its response

## Standout Suggestions
*TODO (Optional):* This is where you can provide information about any standout suggestions that you have attempted.


## Acknowledgements
This project was done as my capstone project for Udacity's Azure ML Engineer. I'd like to give credits to Udacity
for putting together great learning material I've used as a base for this project, as well as 
[Azure's notebook examples](https://github.com/Azure/azureml-examples) that definitely helped me out 
while searching for more material. The [AzureML documentation](https://docs.microsoft.com/en-us/azure/machine-learning/)
was also a great source for code examples whenever I had doubts. I'd also like to mention, that this project
was indeed inspired by a [previous project of mine](https://github.com/renejra/ml-finance-btc), where I used
AWS instead of Azure for predicting Bitcoin prices, and took this time the challenge of improving not only the training, 
tuning and deploying procedures used, but also the data sourcing and processing part to get better results.