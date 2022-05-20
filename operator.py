from kubernetes import client, config

config.load_kube_config()

v1 = client.CustomObjectsApi()

VAR = v1.get_namespaced_custom_object(name="rawat-1",plural="rawats",group="bhupi.com",version="v1",namespace="default")


TEST = eval(VAR["metadata"]["annotations"]["kubectl.kubernetes.io/last-applied-configuration"])

PODNAME = TEST["spec"]["podSpec"]["name"]
IMAGENAME= TEST["spec"]["podSpec"]["image"]
# print(TEST["spec"]["configmapSpec"]["name"])
# print(TEST["spec"]["configmapSpec"]["data"])

v1main = client.CoreV1Api()

# pod_metadata = client.V1ObjectMeta(name=PODNAME)
# pod_container = client.V1Container(name='my_container',image=IMAGENAME)
# pod_spec = client.V1PodSpec(containers=pod_container)
# pod_body = client.V1Pod(metadata=pod_metadata, spec=pod_spec, kind='Pod', api_version='v1')
definition = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
            "name": PODNAME
                },
            "spec": {
            "containers": [{
                "name": "testcontainer",
                "image": IMAGENAME,
                "ports": [{
                   "containerPort": 80,
                }],
            }],
                }
            }
# print(pod_body)
v1main.create_namespaced_pod(namespace="default",body=definition)
