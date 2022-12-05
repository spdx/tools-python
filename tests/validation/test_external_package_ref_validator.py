from typing import List

from src.model.package import ExternalPackageReference, ExternalPackageReferenceCategory
from src.validation.external_package_ref_validator import ExternalPackageRefValidator
from src.validation.validation_message import ValidationMessage


def test_correct_external_package_ref():
    external_package_ref_validator = ExternalPackageRefValidator("2.3")

    external_package_ref = ExternalPackageReference(ExternalPackageReferenceCategory.OTHER, "type", "locator",
                                                    "comment")
    validation_messages: List[ValidationMessage] = external_package_ref_validator.validate_external_package_ref(
        external_package_ref)

    assert validation_messages == []
