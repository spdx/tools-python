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
import re
from typing import List

from spdx.model.package import ExternalPackageRef, ExternalPackageRefCategory
from spdx.validation.uri_validators import validate_url, validate_uri
from spdx.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType

CPE22TYPE_REGEX = r'^c[pP][eE]:/[AHOaho]?(:[A-Za-z0-9._\-~%]*){0,6}$'
CPE23TYPE_REGEX = r'^cpe:2\.3:[aho\*\-](:(((\?*|\*?)([a-zA-Z0-9\-\._]|(\\[\\\*\?!"#$$%&\'\(\)\+,\/:;<=>@\[\]\^`\{\|}~]))+(\?*|\*?))|[\*\-])){5}(:(([a-zA-Z]{2,3}(-([a-zA-Z]{2}|[0-9]{3}))?)|[\*\-]))(:(((\?*|\*?)([a-zA-Z0-9\-\._]|(\\[\\\*\?!"#$$%&\'\(\)\+,\/:;<=>@\[\]\^`\{\|}~]))+(\?*|\*?))|[\*\-])){4}$'
MAVEN_CENTRAL_REGEX = r'^[^:]+:[^:]+(:[^:]+)?$'
NPM_REGEX = r'^[^@]+@[^@]+$'
NUGET_REGEX = r'^[^/]+/[^/]+$'
BOWER_REGEX = r'^[^#]+#[^#]+$'
PURL_REGEX = r'^pkg:.+(\/.+)?\/.+(@.+)?(\?.+)?(#.+)?$'
SWH_REGEX = r'^swh:1:(snp|rel|rev|dir|cnt):[0-9a-fA-F]{40}$'
GITOID_REGEX = r'^gitoid:(blob|tree|commit|tag):(sha1:[0-9a-fA-F]{40}|sha256:[0-9a-fA-F]{64})$'


def validate_external_package_refs(external_package_refs: List[ExternalPackageRef], parent_id: str) -> List[
    ValidationMessage]:
    validation_messages = []
    for external_package_ref in external_package_refs:
        validation_messages.extend(validate_external_package_ref(external_package_ref, parent_id))

    return validation_messages


def validate_external_package_ref(external_package_ref: ExternalPackageRef, parent_id: str) -> List[ValidationMessage]:
    context = ValidationContext(parent_id=parent_id, element_type=SpdxElementType.EXTERNAL_PACKAGE_REF,
                                full_element=external_package_ref)

    category = external_package_ref.category
    locator = external_package_ref.locator
    reference_type = external_package_ref.reference_type

    if category == ExternalPackageRefCategory.SECURITY:
        if reference_type == "cpe22Type":
            return validate_against_regex(locator, CPE22TYPE_REGEX, "cpe22Type", context)
        if reference_type == "cpe23Type":
            return validate_against_regex(locator, CPE23TYPE_REGEX, "cpe23Type", context)
        if reference_type in ["advisory", "fix", "url"]:
            if validate_url(locator):
                return [ValidationMessage(
                    f'externalPackageRef locator of type "{reference_type}" must be a valid URL, but is: {locator}',
                    context)]
            return []
        if reference_type == "swid":
            if validate_uri(locator) or not locator.startswith("swid"):
                return [ValidationMessage(
                    f'externalPackageRef locator of type "swid" must be a valid URI with scheme swid, but is: {locator}',
                    context)]
            return []

        return [ValidationMessage(
            f"externalPackageRef type in category SECURITY must be one of [cpe22Type, cpe23Type, advisory, fix, url, swid], but is: {reference_type}",
            context)]

    if category == ExternalPackageRefCategory.PACKAGE_MANAGER:
        if reference_type == "maven-central":
            return validate_against_regex(locator, MAVEN_CENTRAL_REGEX, "maven-central", context)
        if reference_type == "npm":
            return validate_against_regex(locator, NPM_REGEX, "npm", context)
        if reference_type == "nuget":
            return validate_against_regex(locator, NUGET_REGEX, "nuget", context)
        if reference_type == "bower":
            return validate_against_regex(locator, BOWER_REGEX, "bower", context)
        if reference_type == "purl":
            return validate_against_regex(locator, PURL_REGEX, "purl", context)

        return [ValidationMessage(
            f"externalPackageRef type in category PACKAGE_MANAGER must be one of [maven-central, npm, nuget, bower, purl], but is: {reference_type}",
            context)]

    if category == ExternalPackageRefCategory.PERSISTENT_ID:
        if reference_type == "swh":
            return validate_against_regex(locator, SWH_REGEX, "swh", context)
        if reference_type == "gitoid":
            return validate_against_regex(locator, GITOID_REGEX, "gitoid", context)

        return [ValidationMessage(
            f"externalPackageRef type in category PERSISTENT_ID must be one of [swh, gitoid], but is: {reference_type}",
            context)]

    if category == ExternalPackageRefCategory.OTHER:
        if " " in locator:
            return [ValidationMessage(
                f"externalPackageRef type in category OTHER must contain no spaces, but is: {locator}",
                context)]
        return []



def validate_against_regex(string_to_validate: str, regex: str, type_name: str, context: ValidationContext) -> List[
    ValidationMessage]:
    if not re.match(regex, string_to_validate):
        return [ValidationMessage(
            f'externalPackageRef locator of type "{type_name}" must conform with the regex {regex}, but is: {string_to_validate}',
            context)
        ]

    return []
