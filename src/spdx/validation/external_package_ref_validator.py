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
PURL_REGEX = None  # TODO
SWH_REGEX = r'^swh:1:(snp|rel|rev|dir|cnt):[0-9a-fA-F]{40}$'
GITOID_REGEX = r'^gitoid:(blob|tree|commit|tag):(sha1:[0-9a-fA-F]{40}|sha256:[0-9a-fA-F]{64})$'

def validate_external_package_refs(external_package_refs: List[ExternalPackageRef], parent_id: str) -> List[
    ValidationMessage]:
    validation_messages = []
    for external_package_ref in external_package_refs:
        validation_messages.extend(validate_external_package_ref(external_package_ref, parent_id))

    return validation_messages

def validate_external_package_ref(external_package_ref: ExternalPackageRef, parent_id: str) -> List[ValidationMessage]:
    validation_messages = []
    context = ValidationContext(parent_id=parent_id, element_type=SpdxElementType.EXTERNAL_PACKAGE_REF, full_element=external_package_ref)

    if external_package_ref.category == ExternalPackageRefCategory.SECURITY:
        if external_package_ref.reference_type == "cpe22Type":
            if not re.match(CPE22TYPE_REGEX, external_package_ref.locator):
                validation_messages.append(
                    ValidationMessage(f'externalPackageRef locator of type "cpe22Type" must conform with the regex {CPE22TYPE_REGEX}, but is: {external_package_ref.locator}', context)
                )
        elif external_package_ref.reference_type == "cpe23Type":
            if not re.match(CPE23TYPE_REGEX, external_package_ref.locator):
                validation_messages.append(
                    ValidationMessage(
                        f'externalPackageRef locator of type "cpe23Type" must conform with the regex {CPE23TYPE_REGEX}, but is: {external_package_ref.locator}',
                        context)
                )
        elif external_package_ref.reference_type in ["advisory", "fix", "url"]:
            for message in validate_url(external_package_ref.locator):
                validation_messages.append(
                    ValidationMessage(f'externalPackageRef locator of type "{external_package_ref.reference_type}" {message}', context)
                )
        elif external_package_ref.reference_type == "swid":
            for message in validate_uri(external_package_ref.locator):
                validation_messages.append(
                    ValidationMessage(f'externalPackageRef locator of type "{external_package_ref.reference_type}" {message}',
                                      context)
                )
        else:
            validation_messages.append(
                ValidationMessage(f"externalPackageRef type in category SECURITY must be one of [cpe22Type, cpe23Type, advisory, fix, url, swid], but is: {external_package_ref.reference_type}", context)
            )

    elif external_package_ref.category == ExternalPackageRefCategory.PACKAGE_MANAGER:
        if external_package_ref.reference_type == "maven-central":
            if not re.match(MAVEN_CENTRAL_REGEX, external_package_ref.locator):
                validation_messages.append(
                    ValidationMessage(
                        f'externalPackageRef locator of type "maven-central" must conform with the regex {MAVEN_CENTRAL_REGEX}, but is: {external_package_ref.locator}',
                        context)
                )
        elif external_package_ref.reference_type == "npm":
            if not re.match(NPM_REGEX, external_package_ref.locator):
                validation_messages.append(
                    ValidationMessage(
                        f'externalPackageRef locator of type "npm" must conform with the regex {NPM_REGEX}, but is: {external_package_ref.locator}',
                        context)
                )
        elif external_package_ref.reference_type == "nuget":
            if not re.match(NUGET_REGEX, external_package_ref.locator):
                validation_messages.append(
                    ValidationMessage(
                        f'externalPackageRef locator of type "nuget" must conform with the regex {NUGET_REGEX}, but is: {external_package_ref.locator}',
                        context)
                )
        elif external_package_ref.reference_type == "bower":
            if not re.match(BOWER_REGEX, external_package_ref.locator):
                validation_messages.append(
                    ValidationMessage(
                        f'externalPackageRef locator of type "bower" must conform with the regex {BOWER_REGEX}, but is: {external_package_ref.locator}',
                        context)
                )
        elif external_package_ref.reference_type == "purl":
            pass
        else:
            validation_messages.append(
                ValidationMessage(
                    f"externalPackageRef type in category PACKAGE_MANAGER must be one of [maven-central, npm, nuget, bower, purl], but is: {external_package_ref.reference_type}", context)
            )

    elif external_package_ref.category == ExternalPackageRefCategory.PERSISTENT_ID:
        if external_package_ref.reference_type == "swh":
            if not re.match(SWH_REGEX, external_package_ref.locator):
                validation_messages.append(
                    ValidationMessage(
                        f'externalPackageRef locator of type "swh" must conform with the regex {SWH_REGEX}, but is: {external_package_ref.locator}',
                        context)
                )
        elif external_package_ref.reference_type == "gitoid":
            if not re.match(GITOID_REGEX, external_package_ref.locator):
                validation_messages.append(
                    ValidationMessage(
                        f'externalPackageRef locator of type "gitoid" must conform with the regex {GITOID_REGEX}, but is: {external_package_ref.locator}',
                        context)
                )
        else:
            validation_messages.append(
                ValidationMessage(
                    f"externalPackageRef type in category PERSISTENT_ID must be one of [swh, gitoid], but is: {external_package_ref.reference_type}",
                    context)
            )
    elif external_package_ref.category == ExternalPackageRefCategory.OTHER:
        if " " in external_package_ref.locator:
            validation_messages.append(
                ValidationMessage(f"externalPackageRef type in category OTHER must contain no spaces, but is: {external_package_ref.locator}", context)
            )


    return validation_messages
