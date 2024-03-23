import os
from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
from diagrams.onprem import vcs, ci, client

openapi_img_path = os.path.abspath("openapi/images/openapi.png")
scalar_img_path = os.path.abspath("openapi/images/scalar.png")
postman_img_path = os.path.abspath("openapi/images/postman.png")

with Diagram("API 문서화 CI/CD", filename="img/openapi_cicd_architecture", show=False):
    with Cluster("API 문서화"):
        github = vcs.Github("Protobuf Repository")
        actions = ci.GithubActions("Github Actions")
        postman = Custom("postman", postman_img_path)
        openapi = Custom("openapi", openapi_img_path)
        scalar = Custom("scalar web", scalar_img_path)
        server_developer = client.Users("Server Developer")
        client_developer = client.Users("Client Developer")
        github >> Edge(label="Trigger") >> actions
        actions >> [postman, openapi]
        openapi >> Edge(label="Serve") >> scalar << client_developer
        postman << server_developer

