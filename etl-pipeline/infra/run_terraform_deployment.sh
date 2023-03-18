#!/bin/bash

set -euxo pipefail

INPUT_VARS=${1}

SECRET_OUTPUT_PATH=${2}

CURR_DIR="$(cd -P -- "$(dirname -- "$0")" && pwd -P)"
cd "$CURR_DIR"/terraform

terraform init -input=false

terraform apply -auto-approve -input=false -var-file="$INPUT_VARS"

terraform output -json > $SECRET_OUTPUT_PATH