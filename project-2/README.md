# Operationalizing Machine Learning
This project is part of Udacity's Machine Learning Engineer in Azure nanodegree, and consisted on **using Azure to configure a ML model in production, deploy it with a REST endpoint for consumpion,** test its use **and create and publish a pipeline** that will retrain the model with the use of another REST endpoint.

## Architectural Diagram
![Architecture diagram](assets/architecture-diagram.jpg)

We followed the above architectural diagram during this project in two different procedures, first used the Azure ML Studio platform to go from steps 1-4 manually (mostly in a click-based manner), but we then used a [Jupyter Notebook](aml-pipelines-with-automated-machine-learning-step.ipynb) to create and publish an automated pipeline (step 5) with very similar steps, now using Azure Python SDK. All key steps will be covered below, providing screenshots of all completed steps throughout the process.

## Key Steps
In this section we will deep-dive into all the processes and steps taken in the Azure cloud platform to achieve the project's objectives.

### Registering the Dataset
The data used for this project is the [Bank Marketing Dataset](https://automlsamplenotebookdata.blob.core.windows.net/automl-sample-notebook-data/bankmarketing_train.csv). The dataset was first downloaded and subsequently uploaded into Azure. The image below shows the mentioned dataset correctly uploaded into Azure Machine Learning Studio.

![Uploaded Dataset](assets/dataset-project.jpg)

### Creating a necessary resources

*Compute Cluster:*
Before creating an AutoML run, we need to provision relevant resources. For this we created a Compute Cluster with the following characteristics:
- Min nodes: 1
- Max nodes: 6
- Virtual Machine Size: `Standard_DS12_v2`

*Compute Instance:*
A compute instance was needed to run the [notebook for creating and publishing a pipeline](#creating-and-deploying-a-pipeline). In the respective section we dive deeper in the steps done within this notebook.

### Creating an Automated ML (AutoML) run
Now that we have a dataset for training and a virtual machine to run our experiment, we proceeded to create an AutoML run to try out a variety of models and pick the best performing one. We used the following settings to configure the AutoML run:
- Objective: Classification
- Target column: 'y'
- Exit criterion: 1 hour run
- Concurrency: 5 nodes

With these settings, we ran the experiment successfully as seen in the image below. The **best model ended up being a VotingEnsemble with AUC weighted accuracy of 94.77%.**

![Experiment completed](assets/experiment-completed.jpg)

### Model comparison and metrics
*One of the advantages of using AutoML, is the fact that it tries dozens or even hundreds of models and hyperparameter combinations*, to see what works better for the task at hand. In the image below, we can see which were the best-performing models in this case.

![Models compared](assets/models-compared.jpg)

**A total of 72 models were tried in this run!** This is massive, and here we can see the potential of using AutoML for quick results with machine learning. The top models seen in the image above range from LightGBM, XGBoost, StackEnsembles and (our best-performing model) a VotingEnsemble, each using different normalization steps, and requiring different training time (in the image we see a range from 15 seconds to 2 minutes required for training).

As we mentioned before, the best model in our case was a VotingEnsemble with 94.77% AUC weighted accuracy. We can see more metrics on this model in the image below.

![Best model](assets/best-model.jpg)

It is also possible to go deeper into explaining the best model. For this we needed to check the box `explain best model` before doing the automated run. *One of the most useful features (in my opinion) is to understand what are the most decisive features for our predictions.* In the image below, we see which are the Top 10 features in this regard from our Bank Marketing Dataset. The most important feature to making predictions (in this case) seems to be the duration of clients within the bank.

![Top features](assets/top-features.jpg)

### Model deployment to a REST endpoint
For our best model to be used by other apps or in `production`, we need to make this machine learning model available. A great way to do this is **provisioning predictions through a REST endpoint** using authentication. Doing this with Azure ML takes only a few minutes and a couple clicks, and voilá! You have a managed endpoint for your model. The image below shows the VotingEnsemble model above, deployed correctly to a REST endpoint provisioned through a compute instance.

![Deployed model](assets/deployed-model.jpg)

### Enabling logs with Application Insights
**Application Insights is a log service** that can be enabled both through the Azure ML Studio platform directly, or **using Azure Python SDK**. We used the latter to enable this feature that is commonly used to debug a deployed model. *The code used for this purpose can be found in [`logs.py`](logs.py) file*, which uses a config.json file to get the Workspace details and we pass in the endpoint name in order to activate the logs. In the image below, we can observe that after running `logs.py` file we get some logs responses as expected.

![Application Insights](assets/application-insights.jpg)

We can also see that after running correctly the above script, *we see that Application Insights is correctly set up and running if we inspect the endpoint in Azure ML Studio* (see the last two values from the image - Application Insights Enabled: True).

![App Insights Enabled](assets/application-insights-enabled.jpg)

### Testing the endpoint
In order to test our endpoint, we use the script in [`endpoint.py`](endpoint.py). For this, we needed to replace the endpoint URL and the relevant Bearer Key for authentication. **This script sends in two data points and returns a list of predictions**. The image below shows the mentioned script being ran with PyCharm (a popular Python IDE) and the expected predictions of our endpoints being printed as a response.

![Endpoint Test](assets/endpoint-test.jpg)

### Documenting the endpoint with Swagger
For others to be able to use an endpoint, it's important to document the expected type and fields of your HTTP requests. For this purpose `Swagger` is a great and easy choice greatly supported by Azure. In this project we used it to document our `GET` and `POST` endpoints, by first downloading a [`swagger.json file`](swagger/swagger.json), then running the [`swagger.sh script`](swagger/swagger.sh) that uses Docker to pull and provision a Swagger image, and then using [`serve.py script`](swagger/serve.py) to serve it to a local port. In the image below, you can see the `Swagger` documentation correctly served.

![Swagger Endpoint](assets/swagger-endpoint.jpg)

If you would like to see a longer screenshot of the Swagger documentation created, **feel free to checkout this [bigger screenshot](assets/swagger_endpoints.png) that features the expanded explanations of the `GET` and `POST` endpoints**, but that is not rendered in this README file as it is too long.

### Creating and deploying a pipeline
Before this step, we ran everything directly on the Azure ML Studio platform in a click-based manner, and while it was fairly easy to do so it is not really an automated procedure and it would be time consuming for a developer to retrain a model if, for example, the data changes or gets updated. **Now it's the time to use Azure Python SDK to automate most of what we did**, so if the dataset gets updated or changes, or we simply want to retrain our model after a specific amount of time, we can do so by using a managed REST API endpoint from an Azure Pipeline, **enabling us a whole new set of automated use cases in production**.

All steps followed in this section can be found directly in this [Jupyter Notebook](aml-pipelines-with-automated-machine-learning-step.ipynb) so you can follow step-by-step what happened. In a nutshell, we do the following in the notebook:
- Initialized the Azure Workspace by using a `config.json` file
- Attached the experiment and `compute cluster` created beforehand
- Grabbed the `dataset` registered
- Created automared pipeline steps, including:
    + Configured an AutoML run
    + Setup of output variables (metrics data and best model data)
- Submitted the pipeline. In the image below, we see that the pipeline was submitted for run.
![Pipeline submitted](assets/pipeline-section.jpg)
- Deployed the pipeline to an Azure-managed REST API endppoint. We can see in the image below, that both the prior pipeline run and the deployment of its endpoint both suceeded.
![Pipeline suceeded](assets/pipeline-endpoint.jpg)
- If we check in Azure ML Studio, we see the API endpoint status marked as `active` and its corresponding URL. 
![Endpoint detail](assets/pipeline-endpoint-detail.jpg)
![Endpoint detail](assets/pipeline-endpoint-detail-2.jpg)
- We finally tried out the deployed REST endpoint to run the pipeline using the `Python's requests library`. With the easy use of a `POST` request, we basically submitted a pipeline run triggering the steps registered before. We can see in the image below that this submitted run was completed successfully.
![Pipeline run](assets/pipeline-run-3.jpg)
- The step before can also be inspected directly on the notebook, with the use of the `RunDetails widget` (see image below).
![Widget](assets/pipeline-run-2.jpg)

More details of the process, running pipeline, its endpoint and a live preview of the notebook with a peek on their widgets can also be found in the following section, during a screen recording.

## Screen Recording
In order to demonstrate the above mentioned steps, we also provide a screencast recoding. The video can be found **[in Youtube using this link](https://youtu.be/9bJirgPb3oY) and it features a demo of most of the resources and steps mentioned above**. Hope you like it!

## Standout Suggestions
Since we used the provided Virtual Machines of Udacity to access Azure, the optional section of creating a service principal and authenticate to it was not possible nor relevant. While we also do not provide the optional Apache Benchmark results, we did replace the relevant REST endpoint URI and Bearer Key on the [`benchmark.sh`](benchmark.sh) file script.

## Ideas for project improvement
The work on this project can be improved, of course. Some of the ideas I could think about are:
- **Including a requirements.txt** file to show dependencies and reproduce these experiments.
- **Improving security** by leaving out all secrets from the repository. In this case I intentionally left them, since resources are already destroyed and so reviewers could see the endpoints created as in the images and video. But in a production environment I would use environment variables and take them out of our code.
- Creating a **standalone webapp to serve the Swagger documentation**.
- **Improving the pipeline** or adding more features. Some of these could be for example, retraining after dataset has changed or every certain amount of time upload a new dataset and trigger the pipeline.
- **Exporting the model to ONNX** would enable portability of the model to other devices and platforms. This was also suggested as a standout suggestion from Udacity.