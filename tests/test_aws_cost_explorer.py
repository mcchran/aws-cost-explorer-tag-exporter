from aws_cost_explorer import AwsCostExplorer
from datetime import datetime
from unittest.mock import MagicMock, patch
import pytest

@pytest.fixture
def mock_boto3_client():
    mock_boto3_client = MagicMock()
    # let's update the get_tags mock to have three side effects for each tag
    mock_boto3_client.get_tags.side_effect = [
        {"Tags": ["Tag1"]},
        {"Tags": ["Tag2"]},
    ]
    return mock_boto3_client

@pytest.fixture
def metrics_store():
    return MagicMock()


@pytest.fixture
def aws_cost_explorer(mock_boto3_client, metrics_store):
    tag_list = ['tag1', 'tag2']  # Add your tag list here
    # let's patch the datetime now module
    with patch('aws_cost_explorer.datetime') as mock_datetime:
        mock_datetime.today.return_value =  datetime(2024, 3, 31, 11, 47, 44, 690551)
        with patch('aws_cost_explorer.boto3.client', return_value=mock_boto3_client):
            aws_cost_explorer = AwsCostExplorer(metrics_store, tag_list)
    return aws_cost_explorer

# def test_aws_cost_analyzer_init(aws_cost_explorer, mock_boto3_client):
#     # let's assert that the boto3 client was called twice
#     assert mock_boto3_client.get_tags.call_count == 2
#     mock_boto3_client.get_tags.assert_has_calls([
#         MagicMock(TimePeriod={'Start': '2024-03-30', 'End': '2024-03-31'}, TagKey='tag1'),
#         MagicMock(TimePeriod={'Start': '2024-03-30', 'End': '2024-03-31'}, TagKey='tag2'),
#     ])

    # Assert that the correct values were stored
    # assert aws_cost_explorer.tag_values['tag1'] == ["Tag1"]
    # assert aws_cost_explorer.tag_values['tag2'] == ["Tag2"]
    
# def test_get_daily_costs(aws_cost_explorer, mock_boto3_client, metrics_store):
#     # Mock response from get_cost_and_usage
#     mock_boto3_client.get_cost_and_usage.return_value = {
#         "ResultsByTime": [
#             {
#                 "Total": {
#                     "BlendedCost": {"Amount": 10.5}
#                 }
#             }
#         ]
#     }

#     # Call the method under test
#     aws_cost_explorer.get_daily_costs()

#     # let's assert we have called the method twice with the correct arguments
#     assert mock_boto3_client.get_cost_and_usage.call_count == 2

#     # Assert that the metrics_store's add_metric method was called with the correct arguments
#     metrics_store.add_metric.assert_called_with("tag1", "value1", "BlendedCost", 10.5)

# def test_get_daily_usages(aws_cost_explorer, mock_boto3_client):
#     # Mock response from get_cost_and_usage
#     mock_boto3_client.get_cost_and_usage.return_value = {
#         "ResultsByTime": [
#             {
#                 "Total": {
#                     "UsageQuantity": {"Amount": 20.0}
#                 }
#             }
#         ]
#     }

#     # Call the method under test
#     usages = aws_cost_explorer.get_daily_usages()

#     # Assert that the correct methods were called
#     mock_boto3_client.get_cost_and_usage.assert_called_once()

#     # Assert that the correct value was returned
#     assert usages == 20.0
