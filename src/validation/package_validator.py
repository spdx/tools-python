from typing import List

from src.model.document import Document
from src.model.package import Package
from src.model.relationship import RelationshipType
from src.validation.checksum_validator import ChecksumValidator
from src.validation.external_package_ref_validator import ExternalPackageRefValidator
from src.validation.license_expression_validator import LicenseExpressionValidator
from src.validation.package_verification_code_validator import PackageVerificationCodeValidator
from src.validation.spdx_id_validation import validate_spdx_id
from src.validation.uri_validators import validate_url, validate_package_download_location
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


class PackageValidator:
    spdx_version: str
    document: Document
    license_expression_validator: LicenseExpressionValidator

    def __init__(self, spdx_version: str, document: Document):
        self.spdx_version = spdx_version
        self.document = document
        self.license_expression_validator = LicenseExpressionValidator(spdx_version)

    def validate_packages(self, packages: List[Package]) -> List[ValidationMessage]:
        validation_messages: List[ValidationMessage] = []
        for package in packages:
            validation_messages.extend(self.validate_package(package))

        return validation_messages

    def validate_package(self, package: Package) -> List[ValidationMessage]:
        checksum_validator = ChecksumValidator(self.spdx_version, parent_id=package.spdx_id)
        verification_code_validator = PackageVerificationCodeValidator(self.spdx_version, package.spdx_id)
        external_package_ref_validator = ExternalPackageRefValidator(self.spdx_version, package.spdx_id)

        validation_messages: List[ValidationMessage] = []
        context = ValidationContext(spdx_id=package.spdx_id, parent_id=self.document.creation_info.spdx_id,
                                    element_type=SpdxElementType.PACKAGE, full_element=package)

        for message in validate_spdx_id(package.spdx_id, self.document):
            validation_messages.append(ValidationMessage(message, context))

        download_location = package.download_location
        if isinstance(download_location, str):
            for message in validate_package_download_location(download_location):
                validation_messages.append(ValidationMessage("download_location " + message, context))

        homepage = package.homepage
        if isinstance(homepage, str):
            for message in validate_url(homepage):
                validation_messages.append(ValidationMessage("homepage " + message, context))

        if package.verification_code:
            if not package.files_analyzed:
                validation_messages.append(
                    ValidationMessage(
                        f'verification_code must be None if files_analyzed is False, but is: {package.verification_code}',
                        context))
            else:
                validation_messages.extend(
                    verification_code_validator.validate_verification_code(package.verification_code)
                )

        # TODO: make test for this
        if not package.files_analyzed:
            package_contains_relationships = [relationship for relationship in self.document.relationships if
                                              relationship.relationship_type == RelationshipType.CONTAINS and relationship.spdx_element_id == package.spdx_id]
            if package_contains_relationships:
                validation_messages.append(
                    ValidationMessage(
                        f'package must contain no elements if files_analyzed is False, but found {package_contains_relationships}',
                        context)
                )

            contained_in_package_relationships = [relationship for relationship in self.document.relationships if
                                                  relationship.relationship_type == RelationshipType.CONTAINED_BY and relationship.related_spdx_element_id == package.spdx_id]
            if contained_in_package_relationships:
                validation_messages.append(
                    ValidationMessage(
                        f'package must contain no elements if files_analyzed is False, but found {package_contains_relationships}',
                        context)
                )

        validation_messages.extend(
            checksum_validator.validate_checksums(package.checksums)
        )

        validation_messages.extend(
            self.license_expression_validator.validate_license_expression(package.license_concluded)
        )

        if package.license_info_from_files:
            if not package.files_analyzed:
                validation_messages.append(
                    ValidationMessage(
                        f'license_info_from_files must be None if files_analyzed is False, but is: {package.license_info_from_files}',
                        context)
                )
            else:
                validation_messages.extend(
                    self.license_expression_validator.validate_license_expressions(package.license_info_from_files)
                )

        validation_messages.extend(
            self.license_expression_validator.validate_license_expression(package.license_declared)
        )

        validation_messages.extend(
            external_package_ref_validator.validate_external_package_refs(package.external_references)
        )

        return validation_messages
