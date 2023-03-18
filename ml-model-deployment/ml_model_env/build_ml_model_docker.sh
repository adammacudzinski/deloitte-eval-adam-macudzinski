#!/bin/bash

set -euxo pipefail

CURR_DIR="$(cd -P -- "$(dirname -- "$0")" && pwd -P)"
cd $CURR_DIR

eval $(minikube -p minikube docker-env)

docker build . -t ml_model_env:dev