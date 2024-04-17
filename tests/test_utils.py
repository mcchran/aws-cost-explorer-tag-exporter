from utils import (
    dict_product,
    dict_orthogonal_product,
)

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
    

def test_empty_dict():
    assert dict_orthogonal_product({}) == []

def test_single_key_single_value():
    assert dict_orthogonal_product({'a': [1]}) == [{'a': 1}]

def test_single_key_multiple_values():
    assert dict_orthogonal_product({'a': [1, 2]}) == [{'a': 1}, {'a': 2}]

def test_multiple_keys():
    assert dict_orthogonal_product({'a': [1], 'b': [2]}) == [{'a': 1, 'b': ''}, {'a': '', 'b': 2}]

def test_multiple_keys_multiple_values():
    assert dict_orthogonal_product({'a': [1, 2], 'b': [3, 4]}) == [{'a': 1, 'b': 3}, {'a': 1, 'b': 4}, {'a': 2, 'b': 3}, {'a': 2, 'b': 4}]