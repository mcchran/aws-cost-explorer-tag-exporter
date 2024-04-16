from utils import get_dict_product

def test_get_dict_product():
    # Test case with a dictionary containing 2 tags and 2 values each
    test_dict_1 = {
        'tag1': ['value1', 'value2'], 
        'tag2': ['value3', 'value4']
    }
    expected_result_1 = [
        {'tag1': 'value1', 'tag2': 'value3'},
        {'tag1': 'value1', 'tag2': 'value4'},
        {'tag1': 'value2', 'tag2': 'value3'},
        {'tag1': 'value2', 'tag2': 'value4'}
    ]
    assert get_dict_product(test_dict_1) == expected_result_1