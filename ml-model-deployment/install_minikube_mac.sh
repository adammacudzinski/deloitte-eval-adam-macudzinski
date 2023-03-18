#!/bin/bash

set -euxo pipefail

curl -LO https://github.com/kubernetes/minikube/releases/download/v1.21.0/minikube-darwin-amd64
sudo install minikube-darwin-amd64 /usr/local/bin/minikube