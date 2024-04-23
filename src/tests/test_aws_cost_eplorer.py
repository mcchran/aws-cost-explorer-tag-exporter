from aws_cost_explorer import AWSBlendingCostExplorer
from datetime import datetime
from unittest.mock import MagicMock, patch
import pytest


@pytest.fixture
def mock_ce_client():
    return MagicMock()


def test_get_aws_filters():
    explorer = AWSBlendingCostExplorer(None)
    tag_map = {"tag1": "value1", "tag2": "value2"}
    aws_service = "ec2"
    expected_filter = {
        "And": [
            {"Tags": {"Key": "tag1", "Values": ["value1"]}},
            {"Tags": {"Key": "tag2", "Values": ["value2"]}},
            {
                "Dimensions": {
                    "Key": "SERVICE",
                    "Values": ["ec2"],
                    "MatchOptions": ["EQUALS"],
                }
            },
        ]
    }
    assert explorer._get_aws_filters(aws_service, tag_map) == expected_filter


@patch("aws_cost_explorer.datetime")
def test_get_last_cost_and_usage(mocked_datetime_today, mock_ce_client):
    # hint: since aws updates costs like once per day we get costs two days back 
    # to have the latest accurate value
    mocked_datetime_today.today.return_value = datetime(2024, 4, 23)
    explorer = AWSBlendingCostExplorer(mock_ce_client)
    explorer._get_last_cost_and_usage()
    mock_ce_client.get_cost_and_usage.assert_called_once_with(
        TimePeriod={"Start": "2024-04-20", "End": "2024-04-21"}
    )


@patch("aws_cost_explorer.datetime")
def test_get_costs_for(mocked_datetime_today, mock_ce_client):
    # hint: since aws updates costs like once per day we get costs two days back 
    # to have the latest accurate value
    mocked_datetime_today.today.return_value = datetime(2024, 4, 23)
    explorer = AWSBlendingCostExplorer(mock_ce_client)
    mock_resp = {"ResultsByTime": [{"Total": {"BlendedCost": {"Amount": 100.0}}}]}

    mock_ce_client.get_cost_and_usage.return_value = mock_resp

    aws_service = "ec2"
    tag_map = {"tag1": "value1", "tag2": "value2"}

    assert explorer.get_costs_for(aws_service, tag_map) == 100.0
    mock_ce_client.get_cost_and_usage.assert_called_once_with(
        Granularity="DAILY",
        Metrics=["BlendedCost"],
        Filter={
            "And": [
                {"Tags": {"Key": "tag1", "Values": ["value1"]}},
                {"Tags": {"Key": "tag2", "Values": ["value2"]}},
                {
                    "Dimensions": {
                        "Key": "SERVICE",
                        "Values": ["ec2"],
                        "MatchOptions": ["EQUALS"],
                    }
                },
            ],
        },
        TimePeriod={"Start": "2024-04-20", "End": "2024-04-21"},
    )
