from unittest.mock import MagicMock, patch
import pytest

from aws_service_tag_exporter import AWSServiceTagExporter

@pytest.fixture
def mock_boto3_client():
    with patch("boto3.client") as mock_client:
        yield mock_client

def test_get_resources_with_tags(mock_boto3_client):
    # Mocking boto3 client
    mock_get_resources = MagicMock()
    mock_get_resources.paginate.return_value = [
        {"ResourceTagMappingList": [{"ResourceARN": "arn1", "Tags": [{"Key": "key1", "Value": "value1"}]}]},
        {"ResourceTagMappingList": [{"ResourceARN": "arn2", "Tags": [{"Key": "key2", "Value": "value2"}]}]}
    ]
    mock_boto3_client.return_value.get_paginator.return_value = MagicMock(paginate=mock_get_resources)

    exporter = AWSServiceTagExporter(["tag1", "tag2"])
    resources_with_tags = exporter.get_resources_with_tags()

    assert len(resources_with_tags) == 2
    assert "arn1" in resources_with_tags
    assert "arn2" in resources_with_tags
    assert resources_with_tags["arn1"] == [{"Key": "key1", "Value": "value1"}]
    assert resources_with_tags["arn2"] == [{"Key": "key2", "Value": "value2"}]

def test_get_tags_per_service():
    exporter = AWSServiceTagExporter([])
    resources_with_tags = {
        "arn:aws:service1:resource1": [{"Key": "tag1", "Value": "value1"}, {"Key": "tag2", "Value": "value2"}],
        "arn:aws:service2:resource2": [{"Key": "tag1", "Value": "value1"}, {"Key": "tag3", "Value": "value3"}]
    }
    tags_per_service = exporter.get_tags_per_service(resources_with_tags)

    assert len(tags_per_service) == 2
    assert "service1" in tags_per_service
    assert "service2" in tags_per_service
    assert tags_per_service["service1"]["tag1"] == ["value1"]
    assert tags_per_service["service1"]["tag2"] == ["value2"]
    assert tags_per_service["service2"]["tag1"] == ["value1"]
    assert tags_per_service["service2"]["tag3"] == ["value3"]

def test_get_services_for_tags(mock_boto3_client):
    # Mocking boto3 client
    mock_get_resources = MagicMock()
    mock_get_resources.paginate.return_value = [
        {"ResourceTagMappingList": [{"ResourceARN": "arn:aws:ec2:resource1", "Tags": [{"Key": "tag1", "Value": "value1"}]}]},
        {"ResourceTagMappingList": [{"ResourceARN": "arn:aws:rds:resource2", "Tags": [{"Key": "tag2", "Value": "value2"}]}]}
    ]
    mock_boto3_client.return_value.get_paginator.return_value = MagicMock(paginate=mock_get_resources)

    exporter = AWSServiceTagExporter(["tag1", "tag2"])
    services_with_tags = exporter.get_services_for_tags()

    assert len(services_with_tags) == 2
    assert "Amazon Elastic Compute Cloud - Compute" in services_with_tags
    assert "Amazon Relational Database Service" in services_with_tags
    assert services_with_tags["Amazon Elastic Compute Cloud - Compute"]["tag1"] == ["value1"]
    assert services_with_tags["Amazon Relational Database Service"]["tag2"] == ["value2"]
