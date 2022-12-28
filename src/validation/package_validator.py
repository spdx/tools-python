from typing import List, Optional

from src.model.document import Document
from src.model.package import Package
from src.model.relationship import RelationshipType
from src.validation.checksum_validator import validate_checksums
from src.validation.external_package_ref_validator import validate_external_package_refs
from src.validation.license_expression_validator import validate_license_expression, validate_license_expressions
from src.validation.package_verification_code_validator import validate_verification_code
from src.validation.spdx_id_validators import validate_spdx_id
from src.validation.uri_validators import validate_url, validate_download_location
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


def validate_packages(packages: List[Package], document: Optional[Document] = None) -> List[ValidationMessage]:
    validation_messages: List[ValidationMessage] = []
    if document:
        for package in packages:
            validation_messages.extend(validate_package_within_document(package, document))
    else:
        for package in packages:
            validation_messages.extend(validate_package(package))

    return validation_messages


def validate_package_within_document(package: Package, document: Document) -> List[ValidationMessage]:
    validation_messages: List[ValidationMessage] = []
    context = ValidationContext(spdx_id=package.spdx_id, parent_id=document.creation_info.spdx_id,
                                element_type=SpdxElementType.PACKAGE, full_element=package)

    for message in validate_spdx_id(package.spdx_id, document):
        validation_messages.append(ValidationMessage(message, context))

    # TODO: make test for this
    if not package.files_analyzed:
        package_contains_relationships = [relationship for relationship in document.relationships if
                                          relationship.relationship_type == RelationshipType.CONTAINS and relationship.spdx_element_id == package.spdx_id]
        if package_contains_relationships:
            validation_messages.append(
                ValidationMessage(
                    f"package must contain no elements if files_analyzed is False, but found {package_contains_relationships}",
                    context)
            )

        contained_in_package_relationships = [relationship for relationship in document.relationships if
                                              relationship.relationship_type == RelationshipType.CONTAINED_BY and relationship.related_spdx_element_id == package.spdx_id]
        if contained_in_package_relationships:
            validation_messages.append(
                ValidationMessage(
                    f"package must contain no elements if files_analyzed is False, but found {contained_in_package_relationships}",
                    context)
            )

    validation_messages.extend(validate_package(package, context))

    return validation_messages


def validate_package(package: Package, context: Optional[ValidationContext] = None) -> List[ValidationMessage]:
    validation_messages: List[ValidationMessage] = []
    if not context:
        context = ValidationContext(spdx_id=package.spdx_id, element_type=SpdxElementType.PACKAGE, full_element=package)

    download_location = package.download_location
    if isinstance(download_location, str):
        for message in validate_download_location(download_location):
            validation_messages.append(ValidationMessage("package download_location " + message, context))

    homepage = package.homepage
    if isinstance(homepage, str):
        for message in validate_url(homepage):
            validation_messages.append(ValidationMessage("homepage " + message, context))

    # TODO: is verification_code required if files_analyzed=True? (https://github.com/spdx/tools-python/issues/386)
    verification_code = package.verification_code
    if verification_code:
        if not package.files_analyzed:
            validation_messages.append(
                ValidationMessage(
                    f"verification_code must be None if files_analyzed is False, but is: {verification_code}",
                    context))
        else:
            validation_messages.extend(validate_verification_code(verification_code, package.spdx_id))

    validation_messages.extend(validate_checksums(package.checksums, package.spdx_id))

    validation_messages.extend(validate_license_expression(package.license_concluded))

    license_info_from_files = package.license_info_from_files
    if license_info_from_files:
        if not package.files_analyzed:
            validation_messages.append(
                ValidationMessage(
                    f"license_info_from_files must be None if files_analyzed is False, but is: {license_info_from_files}",
                    context)
            )
        else:
            validation_messages.extend(validate_license_expressions(license_info_from_files))

    validation_messages.extend(validate_license_expression(package.license_declared))

    validation_messages.extend(validate_external_package_refs(package.external_references, package.spdx_id))

    return validation_messages
