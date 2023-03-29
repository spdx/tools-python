# Copyright (c) 2022 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List, Optional

from spdx.model.document import Document
from spdx.model.package import Package
from spdx.model.relationship import RelationshipType, Relationship
from spdx.model.relationship_filters import filter_by_type_and_origin, filter_by_type_and_target
from spdx.validation.checksum_validator import validate_checksums
from spdx.validation.external_package_ref_validator import validate_external_package_refs
from spdx.validation.license_expression_validator import validate_license_expression, validate_license_expressions
from spdx.validation.package_verification_code_validator import validate_verification_code
from spdx.validation.spdx_id_validators import validate_spdx_id
from spdx.validation.uri_validators import validate_url, validate_download_location
from spdx.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


def validate_packages(packages: List[Package], spdx_version: str, document: Optional[Document] = None) -> List[
    ValidationMessage]:
    validation_messages: List[ValidationMessage] = []
    if document:
        for package in packages:
            validation_messages.extend(validate_package_within_document(package, spdx_version, document))
    else:
        for package in packages:
            validation_messages.extend(validate_package(package, spdx_version))

    return validation_messages


def validate_package_within_document(package: Package, spdx_version: str, document: Document) -> List[
    ValidationMessage]:
    validation_messages: List[ValidationMessage] = []
    context = ValidationContext(spdx_id=package.spdx_id, parent_id=document.creation_info.spdx_id,
                                element_type=SpdxElementType.PACKAGE, full_element=package)

    for message in validate_spdx_id(package.spdx_id, document):
        validation_messages.append(ValidationMessage(message, context))

    if not package.files_analyzed:
        package_contains_relationships = filter_by_type_and_origin(document.relationships, RelationshipType.CONTAINS,
                                                                   package.spdx_id)
        contained_in_package_relationships = filter_by_type_and_target(document.relationships,
                                                                       RelationshipType.CONTAINED_BY, package.spdx_id)

        combined_relationships: List[Relationship] = package_contains_relationships + contained_in_package_relationships

        if combined_relationships:
            validation_messages.append(
                ValidationMessage(
                    f"package must contain no elements if files_analyzed is False, but found {combined_relationships}",
                    context)
            )

    validation_messages.extend(validate_license_expression(package.license_concluded, document, package.spdx_id))

    license_info_from_files = package.license_info_from_files
    if license_info_from_files:
        if not package.files_analyzed:
            validation_messages.append(
                ValidationMessage(
                    f"license_info_from_files must be None if files_analyzed is False, but is: {license_info_from_files}",
                    context)
            )
        else:
            validation_messages.extend(validate_license_expressions(license_info_from_files, document, package.spdx_id))

    validation_messages.extend(validate_license_expression(package.license_declared, document, package.spdx_id))

    validation_messages.extend(validate_package(package, spdx_version, context))

    return validation_messages


def validate_package(package: Package, spdx_version: str, context: Optional[ValidationContext] = None) -> List[
    ValidationMessage]:
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

    verification_code = package.verification_code
    if verification_code:
        if not package.files_analyzed:
            validation_messages.append(
                ValidationMessage(
                    f"verification_code must be None if files_analyzed is False, but is: {verification_code}",
                    context))
        else:
            validation_messages.extend(validate_verification_code(verification_code, package.spdx_id))

    validation_messages.extend(validate_checksums(package.checksums, package.spdx_id, spdx_version))

    validation_messages.extend(
        validate_external_package_refs(package.external_references, package.spdx_id, spdx_version))

    if spdx_version == "SPDX-2.2":
        if package.primary_package_purpose is not None:
            validation_messages.append(
                ValidationMessage(f"primary_package_purpose is not supported in SPDX-2.2", context))
        if package.built_date is not None:
            validation_messages.append(
                ValidationMessage(f"built_date is not supported in SPDX-2.2", context))
        if package.release_date is not None:
            validation_messages.append(
                ValidationMessage(f"release_date is not supported in SPDX-2.2", context))
        if package.valid_until_date is not None:
            validation_messages.append(
                ValidationMessage(f"valid_until_date is not supported in SPDX-2.2", context))

        if package.license_concluded is None:
            validation_messages.append(
                ValidationMessage(f"license_concluded is mandatory in SPDX-2.2", context))
        if package.license_declared is None:
            validation_messages.append(
                ValidationMessage(f"license_declared is mandatory in SPDX-2.2", context))
        if package.copyright_text is None:
            validation_messages.append(
                ValidationMessage(f"copyright_text is mandatory in SPDX-2.2", context))

    return validation_messages
