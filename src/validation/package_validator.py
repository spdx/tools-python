from typing import List

from src.model.package import Package
from src.validation.checksum_validator import ChecksumValidator
from src.validation.validation_message import ValidationMessage
from src.validation.external_package_ref_validator import ExternalPackageRefValidator
from src.validation.license_expression_validator import LicenseExpressionValidator



class PackageValidator:
    spdx_version: str
    checksum_validator: ChecksumValidator
    license_expression_validator: LicenseExpressionValidator
    external_package_ref_validator: ExternalPackageRefValidator

    def __init__(self, spdx_version):
        self.spdx_version = spdx_version
        self.checksum_validator = ChecksumValidator(spdx_version)
        self.license_expression_validator = LicenseExpressionValidator(spdx_version)
        self.external_package_ref_validator = ExternalPackageRefValidator(spdx_version)

    def validate_packages(self, packages: List[Package]) -> List[ValidationMessage]:
        error_messages = []
        for package in packages:
            error_messages.extend(self.validate_package(package))

        return error_messages

    def validate_package(self, package: Package) -> List[ValidationMessage]:
        pass
