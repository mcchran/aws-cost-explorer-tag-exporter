from collections import defaultdict
from Levenshtein import distance as levenshtein_distance
import boto3


class AWSServiceTagExporter:

    ALIAS = {
        "cloudfront": "Amazon CloudFront",
        "elasticache": "Amazon ElastiCache",
        "elasticloadbalancing": "Amazon Elastic Load Balancing",
        "rds": "Amazon Relational Database Service",
        "s3": "Amazon Simple Storage Service",
        "ec2": "Amazon Elastic Compute Cloud - Compute",
    }


    def __init__(self, tag_list):
        self.tagging_client = boto3.client("resourcegroupstaggingapi")
        self.tag_list = tag_list

    def get_resources_with_tags(self):
        # Dictionary to store resources and their tags
        resources_with_tags = {}

        # Get resources with tags
        paginator = self.tagging_client.get_paginator("get_resources")
        for response in paginator.paginate():
            for resource in response["ResourceTagMappingList"]:
                resource_arn = resource["ResourceARN"]
                tags = resource["Tags"]
                resources_with_tags[resource_arn] = tags
        return resources_with_tags

    def get_tags_per_service(self, resources_with_tags):
        tags_per_service = defaultdict(lambda: defaultdict(list))
        for arn in resources_with_tags:
            service = arn.split(":")[2]
            for tag_dict in resources_with_tags[arn]:
                tags_per_service[service][tag_dict["Key"]].append(tag_dict["Value"])
        return tags_per_service

    def get_services_for_tags(self):
        resources_with_tags = self.get_resources_with_tags()
        tags_per_service = self.get_tags_per_service(resources_with_tags)
        services_with_tags = defaultdict(lambda: defaultdict(list))
        for service in tags_per_service:
            for tag in self.tag_list:
                if tag in tags_per_service[service]:
                    services_with_tags[self.ALIAS[service]][tag] = list(
                        set(tags_per_service[service][tag])
                    )
        return services_with_tags


if __name__ == "__main__":

    tag_list = ["team", "service"]
    tag_exporter = AWSServiceTagExporter(tag_list)
    
    services_with_tags = tag_exporter.get_services_for_tags()
    print(services_with_tags)
