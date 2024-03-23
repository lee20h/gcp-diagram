import os
from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.vcs import Github
from diagrams.onprem.iac import Atlantis, Terraform
from diagrams.gcp.compute import ComputeEngine
from diagrams.custom import Custom

terragrunt_img_path = os.path.abspath("terraform/images/terragrunt.png")
infracost_img_path = os.path.abspath("terraform/images/infracost.png")

with Diagram("Cloud GitOps", filename="img/terraform_architecture", show=False):
    with Cluster("Apply"):
        apply_git = Github("cloud-formation")
        apply_atlantis = Atlantis("atlantis")
        apply_terraform = Terraform("terraform")

        with Cluster("GCP"):
            resources = [
                ComputeEngine("resource"),
                ComputeEngine("resource"),
                ComputeEngine("resource")
            ]

    apply_git >> Edge(label="atlantis apply") >> apply_atlantis >> apply_terraform >> resources

    with Cluster("Plan"):
        plan_git = Github("cloud-formation")
        plan_atlantis = Atlantis("atlantis")
        plan = [
            Custom("terragrunt", terragrunt_img_path),
            Custom("infracost", infracost_img_path)
        ]
        plan_result_git = Github("cloud-formation")
        plan_git >> Edge(label="atlantis plan") >> plan_atlantis >> plan
        plan >> Edge(label="PR Comment") >> plan_result_git
