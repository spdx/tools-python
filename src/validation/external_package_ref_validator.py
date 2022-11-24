from typing import List

from src.model.package import ExternalPackageReference
from src.validation.checksum_validator import ChecksumValidator
from src.validation.validation_message import ValidationMessage
from src.validation.license_expression_validator import LicenseExpressionValidator


class ExternalPackageRefValidator:
    spdx_version: str
    checksum_validator: ChecksumValidator
    license_expression_validator: LicenseExpressionValidator

    def __init__(self, spdx_version):
        self.spdx_version = spdx_version
        self.checksum_validator = ChecksumValidator(spdx_version)
        self.license_expression_validator = LicenseExpressionValidator(spdx_version)

    def validate_external_package_refs(self, external_package_refs: List[ExternalPackageReference]) -> List[ValidationMessage]:
        error_messages = []
        for external_package_ref in external_package_refs:
            error_messages.extend(self.validate_external_package_ref(external_package_ref))

        return error_messages

    def validate_external_package_ref(self, external_package_ref: ExternalPackageReference) -> List[ValidationMessage]:
        pass
