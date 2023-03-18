import argparse
from kubernetes import client, config
import kfp
import time

from kserve import KServeClient
from kserve import constants
from kserve import V1beta1PredictorSpec
from kserve import V1beta1TFServingSpec
from kserve import V1beta1InferenceServiceSpec
from kserve import V1beta1InferenceService


from kubeflow_pipelines.pipelines.fashion_classifier import train_and_deploy_model


class FashionClassifierModelPipeline:
    storage_class_name = "local-model-volume"
    tf_model_path = "/tf_models"
    pv_name = "model-volume"
    pvc_name = "model-volume-claim"
    pv_access_mode = "ReadWriteMany"

    training_pod_name = "fashion-classifier-training-pod"
    training_container_name = f"{training_pod_name}-container"

    inference_service_name = "fashion-classifier-service"
    inference_deployment_name = "fashion-classifier-deployment"
    inference_service_app = "fashion-classifier-app"
    inference_container_port = 8501
    inference_service_node_port = 31234

    def __init__(self, image_id, host_volume_path, namespace="kubeflow"):
        self.image_id = image_id
        self.host_volume_path = host_volume_path
        self.namespace = namespace

        config.load_kube_config()
        self.api = client.CoreV1Api()

        self.kubeflow_client = kfp.Client(host="http://localhost:3000")

        self.pv = self._get_volume() or self._provision_volumes()
        self.pvc = self._get_volume_claim() or self._provision_volume_claim()

    def _get_volume(self):
        pv_list = self.api.list_persistent_volume().items

        # Check if a persistent volume with a specific name already exists
        for pv in pv_list:
            if pv.metadata.name == self.pv_name:
                return pv

        print(f"Persistent volume {self.pv_name} does not exist.")
        return None

    def _get_volume_claim(self):
        # Get PVC object
        try:
            return self.api.read_namespaced_persistent_volume_claim(name=self.pvc_name, namespace=self.namespace)
        except:
            return None

    def _provision_volumes(self):
        """
        Provision volumes for use in the cluster (store the Model)
        """

        pv = client.V1PersistentVolume(
            api_version="v1",
            kind="PersistentVolume",
            metadata=client.V1ObjectMeta(
                name=self.pv_name
            ),
            spec=client.V1PersistentVolumeSpec(
                capacity={
                    "storage": "10Gi"
                },
                access_modes=[self.pv_access_mode],
                persistent_volume_reclaim_policy="Retain",
                storage_class_name=self.storage_class_name,
                host_path=client.V1HostPathVolumeSource(
                    path=self.host_volume_path
                )
            )
        )

        return self.api.create_persistent_volume(pv)

    def _provision_volume_claim(self):
        """
        Provision volume claim for use in the cluster
        """
        pvc = client.V1PersistentVolumeClaim(
            api_version="v1",
            kind="PersistentVolumeClaim",
            metadata=client.V1ObjectMeta(
                name=self.pvc_name
            ),
            spec=client.V1PersistentVolumeClaimSpec(
                access_modes=[self.pv_access_mode],
                resources={"requests": {"storage": "10Gi"}},
                storage_class_name=self.storage_class_name
            )
        )

        return self.api.create_namespaced_persistent_volume_claim(
            namespace=self.namespace,
            body=pvc
        )

    def wait_for_pod(self, pod):
        """
        Function to wait for a given pod to complete
        """
        pod_name = pod.metadata.name
        while True:
            # Use the read_namespaced_pod_status method to retrieve the status of the pod
            pod_status = self.api.read_namespaced_pod_status(name=pod_name , namespace=self.namespace)

            # Check if the pod has completed running
            if pod_status.status.phase.lower() == 'succeeded':

                print(f'Pod: {pod_name} completed successfully!')
                break
            elif pod_status.status.phase.lower() == 'failed':
                print('Pod failed!')
                raise RuntimeError(f'Pod failed: {pod_name }')
            else:
                print(f'Pod: {pod_name} is continuing to run')
                time.sleep(10)

    def run_training_pod(self):
        """
        Run training Pod by explitly interfacing with K8s via the Python client
        """

        pod_spec = client.V1Pod(
            api_version="v1",
            kind="Pod",
            metadata=client.V1ObjectMeta(
                name=self.training_pod_name,
                namespace=self.namespace
            ),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name=self.training_container_name,
                        image=self.image_id,
                        volume_mounts=[client.V1VolumeMount(
                            name="my-volume",
                            mount_path=self.tf_model_path
                        )],
                        command=["python3"],
                        args=[
                            "/code/python/deloitte-tensorflow/deloitte_tensorflow/scripts/run_fashion_classifier_training.py",
                            "--model_path", f"{self.tf_model_path}/{self.inference_service_name}/0001"
                        ]

                    )
                ],
                volumes=[client.V1Volume(
                    name="my-volume",
                    persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                        claim_name=self.pvc_name
                    )
                )]
            )
        )

        print(f"Deploying Model Training Pod: {self.training_pod_name}")

        self.api.create_namespaced_pod(
            namespace=self.namespace,
            body=pod_spec
        )

    def run_model_deployment(self):
        """
        Run model deployment by explicitly interfacing with K8s via the Python client
        """
        kserve = KServeClient()

        default_model_spec = V1beta1InferenceServiceSpec(
            predictor=V1beta1PredictorSpec(
                tensorflow=V1beta1TFServingSpec(
                    storage_uri=f'pvc://{self.pvc_name}'
                ),
            )
        )

        isvc = V1beta1InferenceService(api_version=constants.KSERVE_V1BETA1,
                                       kind=constants.KSERVE_KIND,
                                       metadata=client.V1ObjectMeta(
                                           name=self.inference_service_name,
                                           namespace=self.namespace
                                       ),
                                       spec=default_model_spec)
        kserve.create(isvc)

    def deploy_tensorflow_serving(self):
        api_client = client.ApiClient()
        api = client.AppsV1Api(api_client)

        deployment_manifest = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": self.inference_deployment_name
            },
            "spec": {
                "selector": {
                    "matchLabels": {
                        "app": self.inference_service_app
                    }
                },
                "replicas": 1,
                "template": {
                    "metadata": {
                        "labels": {
                            "app": self.inference_service_app
                        }
                    },
                    "spec": {
                        "containers": [
                            {
                                "name": "tensorflow-serving",
                                "image": "tensorflow/serving",
                                "ports": [
                                    {
                                        "containerPort": self.inference_container_port
                                    }
                                ],
                                "volumeMounts": [
                                    {
                                        "name": "my-volume",
                                        "mountPath": "/data/models"
                                    }
                                ],
                                "env": [
                                    {
                                        "name": "MODEL_NAME",
                                        "value": self.inference_service_name,
                                    },
                                    {
                                        "name": "MODEL_BASE_PATH",
                                        "value": "/data/models",
                                    },
                                ]

                            }
                        ],
                        "volumes": [
                            {
                                "name": "my-volume",
                                "persistentVolumeClaim": {
                                    "claimName": self.pvc_name
                                }
                            }
                        ]
                    }
                }
            }
        }

        deployment = api.create_namespaced_deployment(namespace=self.namespace, body=deployment_manifest)
        print("Created Deployment: %s" % deployment.metadata.name)

        # Define the Service
        service_manifest = {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "name": self.inference_service_name
            },
            "spec": {
                "selector": {
                    "app": self.inference_service_app
                },
                "ports": [
                    {
                        "name": "http",
                        "protocol": "TCP",
                        "port": 80,
                        "targetPort": self.inference_container_port,
                        "node_port": self.inference_service_node_port
                    }
                ],
                "type": "LoadBalancer"
            }
        }

        # Create the Service
        service = self.api.create_namespaced_service(namespace=self.namespace, body=service_manifest)

    def run_kubeflow_ops_pipeline(self):
        """
        Standard ML Ops pipeline which is managed by Kubeflow Pipeline
        """
        client = kfp.Client(host="http://localhost:3000")

        client.create_run_from_pipeline_func(
            train_and_deploy_model,
            arguments={
                'training_image_id': self.image_id,
                "model_path": self.tf_model_path,
                "pvc": self.pvc_name,
                "model_name": self.inference_service_name
            },
        )

    def run_k8s_ops_pipeline(self):
        """
        Alternative ML Ops pipeline which is achieved by explicitly interfacing with K8s via the Python client
        """
        self.run_training_pod()
        self.deploy_tensorflow_serving()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_id', required=True, help='Tensorflow model training Docker image id')

    args = parser.parse_args()

    pipeline_obj = FashionClassifierModelPipeline(args.image_id, "/data/k8s_volume")

    #pipeline_obj.run_kubeflow_ops_pipeline()

    pipeline_obj.run_k8s_ops_pipeline()
