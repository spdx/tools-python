from typing import List

from src.model.package import Package, PackageVerificationCode
from src.validation.checksum_validator import ChecksumValidator
from src.validation.validation_message import ValidationMessage
from src.validation.external_package_ref_validator import ExternalPackageRefValidator
from src.validation.license_expression_validator import LicenseExpressionValidator


class PackageVerificationCodeValidator:
    spdx_version: str

    def __init__(self, spdx_version):
        self.spdx_version = spdx_version

    def validate_verification_code(self, verification_code: PackageVerificationCode) -> List[ValidationMessage]:
        validation_messages: List[ValidationMessage] = []
        # TODO: implement this and make test for it
        return validation_messages
