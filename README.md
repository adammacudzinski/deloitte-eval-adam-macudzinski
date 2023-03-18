# deloitte-eval-adam-macudzinski

## System Setup

Unfortunately, I didn't have enough time to Dockerize everything
so there are still a few system dependencies required by the two
software projects. 


* **Terraform**:
  * Required to deploy MYSQL RDS instance to AWS
  * https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli
* **Python3.8**:
  * Used as the main data pipeline language https://www.python.org/downloads/
  * https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli
* **poetry**:
  * Python dependency manager
  * https://python-poetry.org/
* **minikube**:
  * Lightweight, local K8s distribution, which we're using to run the ML worklow
  * https://minikube.sigs.k8s.io/docs/start/


## Exercise Breakdown
* **Exercise 1**: [etl-pipeline](etl-pipeline/README.md)
* **Exercise 2**: [ml-model-deployment](ml-model-deployment/README.md)
* **Exercise 3**: [bpc-work-plan](bpc-work-plan)


## Next Steps

### Unit Tests!!! 
### Linting / Formatting / CICD
### Autoscaling