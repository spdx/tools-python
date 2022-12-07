from typing import List

from src.model.package import Package
from src.validation.checksum_validator import ChecksumValidator
from src.validation.package_verification_code_validator import PackageVerificationCodeValidator
from src.validation.validation_message import ValidationMessage
from src.validation.external_package_ref_validator import ExternalPackageRefValidator
from src.validation.license_expression_validator import LicenseExpressionValidator


class PackageValidator:
    spdx_version: str
    checksum_validator: ChecksumValidator
    license_expression_validator: LicenseExpressionValidator
    external_package_ref_validator: ExternalPackageRefValidator
    verification_code_validator: PackageVerificationCodeValidator

    def __init__(self, spdx_version):
        self.spdx_version = spdx_version
        self.checksum_validator = ChecksumValidator(spdx_version)
        self.license_expression_validator = LicenseExpressionValidator(spdx_version)
        self.external_package_ref_validator = ExternalPackageRefValidator(spdx_version)
        self.verification_code_validator = PackageVerificationCodeValidator(spdx_version)

    def validate_packages(self, packages: List[Package]) -> List[ValidationMessage]:
        validation_messages: List[ValidationMessage] = []
        for package in packages:
            validation_messages.extend(self.validate_package(package))

        return validation_messages

    def validate_package(self, package: Package) -> List[ValidationMessage]:
        validation_messages: List[ValidationMessage] = []

        # TODO: check that the package has no files (in relationships) if files_analyzed=False

        validation_messages.extend(
            self.verification_code_validator.validate_verification_code(package.verification_code)
        )

        validation_messages.extend(
            self.checksum_validator.validate_checksums(package.checksums)
        )

        validation_messages.append(
            self.license_expression_validator.validate_license_expression(package.license_concluded)
        )

        if package.license_info_from_files:
            if not package.files_analyzed:
                pass
                # TODO: this must not be!
            else:
                validation_messages.extend(
                    self.license_expression_validator.validate_license_expressions(package.license_info_from_files)
                )

        validation_messages.append(
            self.license_expression_validator.validate_license_expression(package.license_declared)
        )

        validation_messages.extend(
            self.external_package_ref_validator.validate_external_package_refs(package.external_references)
        )

        return validation_messages

    def is_valid_package_download_location(self, download_location: str) -> bool:
        # TODO: implement the convoluted package download location validation
        return True
