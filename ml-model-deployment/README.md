# ML Model Deployment Exercise

## High Level Summary
The goal here was to not only deploy an ML model in inference mode as an API
but to do so in way that establishes a solid, scalable foundation which can
be used for multi-platform deployment. As such, I decided on K8s and Kubeflow
because they offer a very solid framework for building distributed MLOps pipeines,
and KServe goes one step further and makes the inference service management 
experience a no brainer. 

In order to demonstrate the end-to-end pipeline from training to deployment, 
I decided to build a Tensorflow image classification model on top of the 
Fashion MNIST dataset, (which just so happens to be included in Tensorflow).

## Key System Components
* **K8s**: Container orchestration platform which all of the other MLOps tooling
    is build upon.
* **KubeFlow Pipeline**: MLOps-oriented pipeline framework which we're using 
    as the core pipeline scheduler. It also offers a sweet UI which should be
    accessible at `localhost:3000` (The setup script is port forwarding)
* **KServe**: Project in the Kubeflow ecosystem which automates ML Model 
    serving / deployment.
* **Tensorflow**: Powerful deep learning framework which is used as the core
   ML modeling engine.

## Important Scripts

### Environment Setup

[setup_local_k8s.sh](setup_local_k8s.sh)

This script sets up the complete Kubeflow and Kserve environment by deploying 
to the minikube cluster which has been assumed to be already provisioned. It also 
builds the Tensorflow model env Docker image by calling `
ml_model_env/build_ml_model_docker.sh`

`setup_local_k8s.sh`

### Model Training and Inference API Deployment Script

[run_full_deployment_pipeline.sh](run_full_deployment_pipeline.sh)

My original plan was to cleanly deploy the Fashion Classifier API to K8s cleanly via a Kubeflow
pipeline, but unfortunately I had to deal with some major version incompatibility issues, so I
reverted to deploying the API as a standard k8s deployment, which appears to be working pretty 
well all things considered. But rather than throw the initial kubeflow pipeline away, I decided
to keep it around as an optional configuration. Maybe it will work one day.

Anyways, this script runs the "functional" pipeline by default

`run_full_deployment_pipeline.sh`

### Kubeflow Pipeline File

[kubeflow/kubeflow_pipelines/kubeflow_pipelines/pipelines/fashion_classifier.py](ml-model-deployment/kubeflow/kubeflow_pipelines/kubeflow_pipelines/pipelines/fashion_classifier.py)

This file defines the Kubeflow Pipeline mentioned above


### Fashion Classifier API client
[ml_model_env/python/deloitte-tensorflow/deloitte_tensorflow/fashion_classifier_client.py](ml_model_env/python/deloitte-tensorflow/deloitte_tensorflow/fashion_classifier_client.py)




