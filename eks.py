from kubernetes import client, config

# Load Kubernetes configuration
config.load_kube_config()

# Create a Kubernetes API client
api_client = client.ApiClient()

# Define the deployment
deployment = client.V1Deployment(
    metadata=client.V1ObjectMeta(name="my-flask-app"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={"app": "my-flask-app"}
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={"app": "my-flask-app"}
            ),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="my-flask-container",
                        image="779846823014.dkr.ecr.ap-south-1.amazonaws.com/my_monitoring_app_image:latest",
                        ports=[client.V1ContainerPort(container_port=5000)]
                    )
                ]
            )
        )
    )
)

# Create the deployment
api_instance = client.AppsV1Api(api_client)
try:
    api_instance.create_namespaced_deployment(
        namespace="default",
        body=deployment
    )
except client.exceptions.ApiException as e:
    if e.status == 409:
        print("Deployment already exists, skipping creation.")
    else:
        raise

# Define the service with LoadBalancer type
service = client.V1Service(
    metadata=client.V1ObjectMeta(name="my-flask-service"),
    spec=client.V1ServiceSpec(
        selector={"app": "my-flask-app"},
        ports=[client.V1ServicePort(port=5000, target_port=5000)],
        type="LoadBalancer"  # Set the service type to LoadBalancer
    )
)

# Create the service
api_instance = client.CoreV1Api(api_client)
try:
    api_instance.create_namespaced_service(
        namespace="default",
        body=service
    )
except client.exceptions.ApiException as e:
    if e.status == 409:
        print("Service already exists, skipping creation.")
    else:
        raise