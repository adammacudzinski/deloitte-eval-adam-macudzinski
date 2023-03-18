#!/bin/bash

set -euxo pipefail

CURR_DIR="$(cd -P -- "$(dirname -- "$0")" && pwd -P)"
cd "$CURR_DIR"

export PIPELINE_VERSION=1.8.5

# Namespace for inference API
kubectl create namespace model-api --dry-run=client -o yaml | kubectl apply -f -

# Install kubeflow pipeline
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io

kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic-pns?ref=$PIPELINE_VERSION"

sleep 30

kubectl wait --namespace=kubeflow --for=condition=Ready pod -l app=ml-pipeline-persistenceagent --timeout=30m
kubectl wait --namespace=kubeflow --for=condition=Ready pod -l app=ml-pipeline --timeout=30m

# Install dependency of kserve: cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.3.0/cert-manager.yaml

# Install dependency of kserve: knative
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.9.2/serving-crds.yaml

# Install kserve to serve the Tensorflow model
while ! kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.10.0/kserve.yaml; do sleep 2; done
while ! kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.10.0/kserve-runtimes.yaml; do sleep 2; done
kubectl patch configmap/inferenceservice-config -n kserve --type=strategic -p \
  '{"data": {"deploy": "{\"defaultDeploymentMode\": \"RawDeployment\"}"}}'
kubectl wait --namespace=kserve --for=condition=Ready pod --timeout=10m --all

kubectl apply -f ${CURR_DIR}/manifests/inferenceservice_permissions.yaml

kubectl port-forward --namespace kubeflow svc/ml-pipeline-ui 3000:80 &