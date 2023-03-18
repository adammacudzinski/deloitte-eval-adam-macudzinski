#!/bin/bash

set -euxo pipefail

CURR_DIR="$(cd -P -- "$(dirname -- "$0")" && pwd -P)"

# In order to activate the poetry shell
KUBEFLOW_PIPELINE_DIR="$CURR_DIR"/kubeflow/kubeflow_pipelines
cd $KUBEFLOW_PIPELINE_DIR

poetry run python3 $KUBEFLOW_PIPELINE_DIR/kubeflow_pipelines/scripts/run_fashion_classifier_pipeline.py \
  --image_id ml_model_env:dev
