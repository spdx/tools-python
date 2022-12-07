from src.validation.string_type_validators import is_valid_uri, is_valid_spdx_id, is_valid_package_download_location

import pytest

# TODO: refine these tests


@pytest.mark.parametrize("input_value", ["test"])
def test_correct_uri(input_value):
    test_result = is_valid_uri(input_value)

    assert test_result is True
    

@pytest.mark.parametrize("input_value", ["test"])
def test_wrong_uri(input_value):
    test_result = is_valid_uri(input_value)
    
    assert test_result is False
    
    
@pytest.mark.parametrize("input_value", ["test"])
def test_correct_internal_spdx_id(input_value):
    test_result = is_valid_spdx_id(input_value)
    
    assert test_result is True
    
    
@pytest.mark.parametrize("input_value", ["test"])
def test_wrong_internal_spdx_id(input_value):
    test_result = is_valid_spdx_id(input_value)
    
    assert test_result is False


@pytest.mark.parametrize("input_value", ["test"])
def test_correct_external_spdx_id(input_value):
    test_result = is_valid_spdx_id(input_value, may_be_external=True)

    assert test_result is True


@pytest.mark.parametrize("input_value", ["test"])
def test_wrong_external_spdx_id(input_value):
    test_result = is_valid_spdx_id(input_value, may_be_external=True)

    assert test_result is False


@pytest.mark.parametrize("input_value", ["test"])
def test_correct_package_download_location(input_value):
    test_result = is_valid_package_download_location(input_value)

    assert test_result is True


@pytest.mark.parametrize("input_value", ["test"])
def test_wrong_package_download_location(input_value):
    test_result = is_valid_package_download_location(input_value)

    assert test_result is False
