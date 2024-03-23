from diagrams import Cluster, Diagram, Edge
from diagrams.onprem import client, queue, workflow
from diagrams.saas.chat import Slack
from diagrams.programming.language import Python, Bash
from diagrams.k8s.compute import Pod

with Diagram("Slack App Architecture", filename="img/slack_architecture", show=False):
    with Cluster("Slack interface"):
        users = client.Users("Users")
        slack = Slack("Slack")
        app = Python("Slack App")
        users >> Edge(label="Command || Mention") >> slack >> Edge(label="Request") >> app
        app >> Edge(label="Response") >> slack >> Edge(label="Chat Message") >> users

    with Cluster("Streaming"):
        kafka = queue.Kafka("kafka")
        app >> Edge(label="Event", style="dashed") >> kafka
        kafka >> Edge(label="Result", style="dashed") >> app

    with Cluster("Batch"):
        airflow = workflow.Airflow("airflow")
        job = [
            Python("Task"),
            Bash("Task"),
            Pod("Task"),
        ]
        app >> Edge(label="Event") >> airflow >> Edge(label="Trigger & Manage") >> job
        airflow >> Edge(label="Result") >> app

    kafka >> Edge(label="Trigger", style="dashed") >> airflow
