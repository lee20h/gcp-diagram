from diagrams import Cluster, Diagram
from diagrams.onprem import network as onprem_network
from diagrams.k8s import network as k8s_network, compute as k8s_compute, clusterconfig as k8s_clusterconfig


with Diagram("K8s", filename="img/k8s_architecture", show=False):
    with Cluster("Service Mesh"):
        istio = onprem_network.Istio("Istio")
        with Cluster("Network"):
            ingressGateway = k8s_network.Ingress("Ingress Gateway")
            virtualService = k8s_network.SVC("Virtual Service")
            service = k8s_network.SVC("Service")
            endpoint = k8s_network.Endpoint("Endpoint")
        ingressGateway >> virtualService >> service >> endpoint
        with Cluster("Compute"):
            deployment = k8s_compute.Deployment("Deployment")
            hpa = k8s_clusterconfig.HPA("HPA")
            pods = [
                k8s_compute.Pod("Pod"),
                k8s_compute.Pod("Pod"),
                k8s_compute.Pod("Pod")
            ]
        endpoint >> pods << deployment << hpa
