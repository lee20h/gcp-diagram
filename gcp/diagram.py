from diagrams import Cluster, Diagram, Edge
from diagrams.gcp import compute, network, database, security, storage

with Diagram("GCP", filename="img/gcp_architecture", show=False):
    with Cluster("Public"):
        with Cluster("Network"):
            dns = network.DNS("Cloud DNS")
            ingress_external_ip = network.ExternalIpAddresses("Ingress External IP")
            egress_external_ip = network.ExternalIpAddresses("Egress External IP")
            nat_gateway = network.NAT("NAT Gateway")
        with Cluster("Security"):
            certMap = security.SecurityCommandCenter("Certificate Map")
        with Cluster("Routing"):
            lb = network.LoadBalancing("Network Load Balancer")
            GCP_Network = network.Network("Target Proxy & URL Map")

    dns >> ingress_external_ip
    ingress_external_ip >> certMap >> lb >> GCP_Network

    with Cluster("VPC"):
        with Cluster("Workloads"):
            gke = compute.GKE("GKE")
            gce = compute.GCE("Compute Engine")
        with Cluster("Database"):
            db = database.SQL("Cloud SQL")

    GCP_Network >> Edge(label="Ingress") >> gke >> gce
    gke >> Edge(label="Egress") >> nat_gateway >> egress_external_ip
    gce >> db
