import kfp.dsl as dsl
from kfp import components


kserve_op = components.load_component_from_url(
    'https://raw.githubusercontent.com/kubeflow/pipelines/master/components/kserve/component.yaml'
)


@dsl.pipeline(
    name="fashion_classifier_training",
    description="Train Fashion MNIST classifier model from scratch"
)
def train_and_deploy_model(
        training_image_id: str,
        model_path: str,
        pvc: str,
        model_name: str
):

    train = dsl.ContainerOp(
        name='model_training',
        # image needs to be a compile-time string
        image=training_image_id,
        command="python3",
        arguments=[
            "/code/python/deloitte-tensorflow/deloitte_tensorflow/scripts/run_fashion_classifier_training.py",
            "--model_path", f"{model_path}/{model_name}/0001"
        ],
        pvolumes={model_path: dsl.PipelineVolume(pvc=pvc)}
    )

    api_deployment = kserve_op(
        action='apply',
        model_name=model_name,
        model_uri=f"pvc://{pvc}",
        framework='tensorflow',
        namespace="kubeflow"
    )
    api_deployment.after(train)
