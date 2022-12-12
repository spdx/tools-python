from src.validation.uri_validator import is_valid_uri

import pytest

# TODO: implement these tests


@pytest.mark.parametrize("input_value", ["test"])
def test_correct_uri(input_value):
    test_result = is_valid_uri(input_value)

    assert test_result is True
    

@pytest.mark.parametrize("input_value", ["test"])
def test_wrong_uri(input_value):
    test_result = is_valid_uri(input_value)
    
    assert test_result is False

