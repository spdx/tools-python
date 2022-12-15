from typing import List

import pytest

from src.model.package import ExternalPackageRef, ExternalPackageRefCategory
from src.validation.external_package_ref_validator import ExternalPackageRefValidator
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.valid_defaults import get_external_package_ref


def test_valid_external_package_ref():
    external_package_ref_validator = ExternalPackageRefValidator("2.3", "SPDXRef-Package")

    external_package_ref = ExternalPackageRef(ExternalPackageRefCategory.OTHER, "swh",
                                              "swh:1:cnt:94a9ed024d3859793618152ea559a168bbcbb5e2", "comment")
    validation_messages: List[ValidationMessage] = external_package_ref_validator.validate_external_package_ref(
        external_package_ref)

    assert validation_messages == []


@pytest.mark.parametrize("external_package_ref, expected_message",
                         [(get_external_package_ref(),
                           "TBD"),
                          ])
@pytest.mark.skip("add tests once external package ref validation is implemented")
def test_invalid_external_package_ref(external_package_ref, expected_message):
    parent_id = "SPDXRef-Package"
    external_package_ref_validator = ExternalPackageRefValidator("2.3", parent_id)
    validation_messages: List[ValidationMessage] = external_package_ref_validator.validate_external_package_ref(
        external_package_ref)

    expected = ValidationMessage(expected_message,
                                 ValidationContext(parent_id=parent_id,
                                                   element_type=SpdxElementType.EXTERNAL_PACKAGE_REF,
                                                   full_element=external_package_ref))

    assert validation_messages == [expected]
