#!/bin/bash

set -euxo pipefail

sudo apt-get install -y --no-install-recommends \
  python3.8 \
  python3-pip \
  libcurl4-openssl-dev \
  libssl-dev \
  python3-dev \
  python3-opengl

if ! command -v poetry &> /dev/null
then
    echo "poetry could not be found, installing"

    curl -sSL https://install.python-poetry.org | python3 -
    # shellcheck disable=SC1090,SC1091
    export PATH="$HOME/.local/bin:$PATH"
fi

poetry config virtualenvs.create false

cd python/deloitte-tensorflow

poetry install --no-interaction

