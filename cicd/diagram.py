from diagrams import Cluster, Diagram, Edge
from diagrams.onprem import ci, gitops, container, vcs
from diagrams.gcp import devtools
from diagrams.saas import chat
from diagrams.gcp.compute import GKE
from diagrams.onprem.ci import Jenkins

with Diagram("초창기 CI\/CD", filename="img/first_cicd_architecture", show=False):
    with Cluster("CD"):
        cd_jenkins = Jenkins("Jenkins")
        first_gen_k8s_control_plane = GKE("Control plane")
        first_gen_cd_Slack = chat.Slack("Slack")
        cd_jenkins >> Edge(label="Deploy") >> first_gen_k8s_control_plane >> Edge(label="Alert", style="dashed") \
        >> first_gen_cd_Slack
    with Cluster("CI"):
        first_gen_git = vcs.Github("Source Repository")
        ci_jenkins = Jenkins("Jenkins")
        first_gen_docker = container.Docker("Docker")
        first_gen_gcr = devtools.ContainerRegistry("Container Registry")
        first_gen_ci_Slack = chat.Slack("Slack")
        first_gen_git >> Edge(label="Webhook") >> ci_jenkins >> Edge(label="Build") >> first_gen_docker \
        >> Edge(label="Push") >> first_gen_gcr >> Edge(label="Alert", style="dashed") >> first_gen_ci_Slack

with Diagram("CI\/CD", filename="img/cicd_architecture", show=False):
    with Cluster("CD"):
        argocd = gitops.Argocd("Argocd")
        gitopsRepo = vcs.Github("Target Repository")
        k8sControlPlane = GKE("Control plane")
        CDSlack = chat.Slack("CD Slack")
        gitopsRepo << Edge(label="Pull") << argocd >> Edge(label="Deploy") \
        >> k8sControlPlane >> Edge(label="alert", style="dashed") >> CDSlack

    with Cluster("CI"):
        git = vcs.Github("Source Repository")
        actions = ci.GithubActions("Github Actions")
        docker = container.Docker("Docker")
        gcr = devtools.ContainerRegistry("Container Registry")
        CISlack = chat.Slack("CI Slack")
        target_repository = vcs.Github("Target Repository")
        git >> Edge(label="Trigger") >> actions >> Edge(label="Build") >> docker >> Edge(label="Push") >> gcr >> Edge(
            label="Commit", style="dashed") \
        >> target_repository >> Edge(label="alert", style="dashed") >> CISlack
