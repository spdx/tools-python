from typing import List

from src.model.package import ExternalPackageRef
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

    def validate_external_package_refs(self, external_package_refs: List[ExternalPackageRef]) -> List[ValidationMessage]:
        validation_messages = []
        for external_package_ref in external_package_refs:
            validation_messages.extend(self.validate_external_package_ref(external_package_ref))

        return validation_messages

    def validate_external_package_ref(self, external_package_ref: ExternalPackageRef) -> List[ValidationMessage]:
        # TODO: this is gonna be insane (Annex F)
        pass
