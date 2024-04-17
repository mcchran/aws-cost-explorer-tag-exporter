from collections import defaultdict
from Levenshtein import distance as levenshtein_distance
import boto3

ALIAS = {
    "cloudfront" : "Amazon CloudFront",
    "elasticache": "Amazon ElastiCache",
    "elasticloadbalancing": "Amazon Elastic Load Balancing",
    "rds" : "Amazon Relational Database Service",
    "s3" :  "Amazon Simple Storage Service",
    "ec2": "Amazon Elastic Compute Cloud - Compute",
}
AWS_SERVICES = [
        "AWS Amplify",
        "Amazon API Gateway",
        "APN Annual Program Fee",
        "Amazon Athena",
        "AWS Backup",
        "Amazon Bedrock",
        "AWS Budgets",
        "Claude (Amazon Bedrock Edition)",
        "AWS CloudFormation",
        "Amazon CloudFront",
        "AWS CloudShell",
        "AWS CloudTrail",
        "AmazonCloudWatch",
        "CloudWatch Events",
        "AWS CodeArtifact",
        "CodeBuild",
        "AWS CodePipeline",
        "Amazon Cognito",
        "AWS Compute Optimizer",
        "AWS Config",
        "AWS Cost Explorer",
        "Crossbeam Partner Ecosystem Platform",
        "AWS Data Transfer",
        "Amazon DataZone",
        "Amazon DevOps Guru",
        "AWS Directory Service",
        "AWS Database Migration Service",
        "Amazon DocumentDB (with MongoDB compatibility)",
        "Amazon DynamoDB",
        "EC2 - Other",
        "Amazon EC2 Container Registry (ECR)",
        "Amazon Elastic Compute Cloud - Compute",
        "Amazon Elastic Container Service for Kubernetes",
        "Amazon Elastic File System",
        "Amazon Elastic Load Balancing",
        "Amazon ElastiCache",
        "AWS Glue",
        "Grafana Cloud observability: Grafana, Prometheus metrics, logs, traces",
        "Amazon GuardDuty",
        "Amazon Inspector",
        "AWS IoT",
        "Jurassic-2 Mid (Amazon Bedrock Edition)",
        "Jurassic-2 Ultra (Amazon Bedrock Edition)",
        "AWS Key Management Service",
        "Amazon Kinesis",
        "AWS Lambda",
        "Amazon Location Service",
        "Amazon Managed Grafana",
        "Amazon Managed Streaming for Apache Kafka",
        "Meta Llama 2 Chat 13B (Amazon Bedrock Edition)",
        "Meta Llama 2 Chat 70B (Amazon Bedrock Edition)",
        "AWS Migration Hub Refactor Spaces",
        "nOps Cloud Management Platform",
        "OCBCloudFront",
        "Amazon Personalize",
        "AWS Premium Support",
        "Amazon Redshift",
        "Refund",
        "Amazon Registrar",
        "Amazon Relational Database Service",
        "Amazon Route 53",
        "Amazon Simple Storage Service",
        "Amazon SageMaker",
        "Savings Plans for AWS Compute usage",
        "AWS Secrets Manager",
        "AWS Security Hub",
        "AWS Service Catalog",
        "Amazon Simple Email Service",
        "Amazon SimpleDB",
        "Snowflake Capacity",
        "Amazon Simple Notification Service",
        "Amazon Simple Queue Service",
        "Squadcast",
        "AWS Step Functions",
        "AWS Support (Enterprise)",
        "AWS Systems Manager",
        "Tackle Cloud GTM Platform",
        "Tax",
        "AWS Transfer Family",
        "Amazon Virtual Private Cloud",
        "AWS WAF",
        "AWS X-Ray",
        "ZoomInfo",
    ]

def get_closest_service(service):
    # let's create a dictionary to store the services and their distances
    services_distances = {}
    # let's iterate over the AWS_SERVICES list
    for aws_service in AWS_SERVICES:
        # let's calculate the distance between the service and the aws_service
        distance = min([
             levenshtein_distance(service.upper(), aws_service_term)
             for aws_service_term in aws_service.split(" ")
        ])
        # let's store the distance in the services_distances dictionary
        services_distances[aws_service] = distance
    # let's get the service with the minimum distance
    closest_service = min(services_distances, key=services_distances.get)
    return closest_service

def get_resources_with_tags(tagging_client):
    # Dictionary to store resources and their tags
    resources_with_tags = {}

    # Get resources with tags
    paginator = tagging_client.get_paginator("get_resources")
    for response in paginator.paginate():
        for resource in response["ResourceTagMappingList"]:
            resource_arn = resource["ResourceARN"]
            tags = resource["Tags"]
            resources_with_tags[resource_arn] = tags
    return resources_with_tags


def get_tags_per_service(resources_with_tags):
    tags_per_service = defaultdict(lambda: defaultdict(list))
    for arn in resources_with_tags:
        service = arn.split(":")[2]
        for tag_dict in resources_with_tags[arn]:
            tags_per_service[service][tag_dict["Key"]].append(tag_dict["Value"])
    return tags_per_service


def get_services_for_tags(tag_list, tagging_client):
    resources_with_tags = get_resources_with_tags(tagging_client)
    tags_per_service = get_tags_per_service(resources_with_tags)
    services_with_tags = defaultdict(lambda: defaultdict(list))
    for service in tags_per_service:
        for tag in tag_list:
            if tag in tags_per_service[service]:
                services_with_tags[ALIAS[service]][tag] = list(set(tags_per_service[service][tag]))
    return services_with_tags


if __name__ == "__main__":
    tagging_client = boto3.client("resourcegroupstaggingapi")

    tag_list = ["team", "service"]
    services_with_tags = get_services_for_tags(tag_list, tagging_client)
    print(services_with_tags)
