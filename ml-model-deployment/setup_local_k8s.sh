#!/bin/bash

set -euxo pipefail

K8S_CLUSTER_CPU=5
K8S_CLUSTER_MEMORY=10000

minikube start --cpus "${K8S_CLUSTER_CPU}" --memory "${K8S_CLUSTER_MEMORY}"

./kubeflow/install_kubeflow.sh

./ml_model_env/build_ml_model_docker.sh