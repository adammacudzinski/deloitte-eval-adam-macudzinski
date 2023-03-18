#!/bin/bash

set -euxo pipefail

INPUT_TF_VARS=${1}

SECRET_TF_OUTPUT_PATH=${2}

EXCEL_FILE_PATH=${3}

CURR_DIR="$(cd -P -- "$(dirname -- "$0")" && pwd -P)"
cd "$CURR_DIR"

export PATH=$PATH:/usr/local/mysql/bin

# Deploy MYSQL RDS DB to AWS
./infra/run_terraform_deployment.sh $INPUT_TF_VARS $SECRET_TF_OUTPUT_PATH

cd "$CURR_DIR"/python

poetry install

# Ingest Excel data into DB
poetry run python3 etl_pipelines/user_data_pipeline.py \
  --excel_file_path $EXCEL_FILE_PATH \
  --secrets_json_file $SECRET_TF_OUTPUT_PATH \
  --batch_id $(date +%F)
