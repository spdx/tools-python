# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import re

import uritools
from beartype.typing import Dict, List

from spdx_tools.spdx.model import ExternalPackageRef, ExternalPackageRefCategory
from spdx_tools.spdx.model.package import CATEGORY_TO_EXTERNAL_PACKAGE_REF_TYPES
from spdx_tools.spdx.validation.uri_validators import validate_url
from spdx_tools.spdx.validation.validation_message import SpdxElementType, ValidationContext, ValidationMessage

CPE22TYPE_REGEX = r"^c[pP][eE]:/[AHOaho]?(:[A-Za-z0-9._\-~%]*){0,6}$"
CPE23TYPE_REGEX = (
    r'^cpe:2\.3:[aho\*\-](:(((\?*|\*?)([a-zA-Z0-9\-\._]|(\\[\\\*\?!"#$$%&\'\(\)\+,\/:;<=>@\[\]\^'
    r"`\{\|}~]))+(\?*|\*?))|[\*\-])){5}(:(([a-zA-Z]{2,3}(-([a-zA-Z]{2}|[0-9]{3}))?)|[\*\-]))(:(((\?*"
    r'|\*?)([a-zA-Z0-9\-\._]|(\\[\\\*\?!"#$$%&\'\(\)\+,\/:;<=>@\[\]\^`\{\|}~]))+(\?*|\*?))|[\*\-])){4}$'
)
MAVEN_CENTRAL_REGEX = r"^[^:]+:[^:]+(:[^:]+)?$"
NPM_REGEX = r"^[^@]+@[^@]+$"
NUGET_REGEX = r"^[^/]+/[^/]+$"
BOWER_REGEX = r"^[^#]+#[^#]+$"
PURL_REGEX = r"^pkg:.+(\/.+)?\/.+(@.+)?(\?.+)?(#.+)?$"
SWH_REGEX = r"^swh:1:(snp|rel|rev|dir|cnt):[0-9a-fA-F]{40}$"
GITOID_REGEX = r"^gitoid:(blob|tree|commit|tag):(sha1:[0-9a-fA-F]{40}|sha256:[0-9a-fA-F]{64})$"

TYPE_TO_REGEX: Dict[str, str] = {
    "cpe22Type": CPE22TYPE_REGEX,
    "cpe23Type": CPE23TYPE_REGEX,
    "maven-central": MAVEN_CENTRAL_REGEX,
    "npm": NPM_REGEX,
    "nuget": NUGET_REGEX,
    "bower": BOWER_REGEX,
    "purl": PURL_REGEX,
    "swh": SWH_REGEX,
    "gitoid": GITOID_REGEX,
}


def validate_external_package_refs(
    external_package_refs: List[ExternalPackageRef], parent_id: str, spdx_version: str
) -> List[ValidationMessage]:
    validation_messages = []
    for external_package_ref in external_package_refs:
        validation_messages.extend(validate_external_package_ref(external_package_ref, parent_id, spdx_version))

    return validation_messages


def validate_external_package_ref(
    external_package_ref: ExternalPackageRef, parent_id: str, spdx_version: str
) -> List[ValidationMessage]:
    validation_messages = []
    context = ValidationContext(
        parent_id=parent_id, element_type=SpdxElementType.EXTERNAL_PACKAGE_REF, full_element=external_package_ref
    )

    category = external_package_ref.category
    locator = external_package_ref.locator
    reference_type = external_package_ref.reference_type

    if category == ExternalPackageRefCategory.OTHER:
        if " " in locator:
            validation_messages.append(
                ValidationMessage(
                    f"externalPackageRef locator in category OTHER must contain no spaces, but is: {locator}", context
                )
            )

    elif spdx_version == "SPDX-2.2" and reference_type in ["advisory", "fix", "url", "swid"]:
        return [ValidationMessage(f'externalPackageRef type "{reference_type}" is not supported in SPDX-2.2', context)]

    elif reference_type not in CATEGORY_TO_EXTERNAL_PACKAGE_REF_TYPES[category]:
        validation_messages.append(
            ValidationMessage(
                f"externalPackageRef type in category {category.name} must be one of "
                f"{CATEGORY_TO_EXTERNAL_PACKAGE_REF_TYPES[category]}, but is: {reference_type}",
                context,
            )
        )

    elif reference_type in ["advisory", "fix", "url"]:
        if validate_url(locator):
            validation_messages.append(
                ValidationMessage(
                    f'externalPackageRef locator of type "{reference_type}" must be a valid URL, but is: {locator}',
                    context,
                )
            )

    elif reference_type == "swid":
        if not uritools.isuri(locator) or not locator.startswith("swid"):
            validation_messages.append(
                ValidationMessage(
                    f'externalPackageRef locator of type "swid" must be a valid URI with scheme swid, '
                    f"but is: {locator}",
                    context,
                )
            )

    else:
        validation_messages.extend(validate_against_regex(locator, reference_type, context))

    return validation_messages


def validate_against_regex(
    string_to_validate: str, reference_type: str, context: ValidationContext
) -> List[ValidationMessage]:
    regex = TYPE_TO_REGEX[reference_type]
    if not re.match(regex, string_to_validate):
        return [
            ValidationMessage(
                f'externalPackageRef locator of type "{reference_type}" must conform with the regex {regex}, '
                f"but is: {string_to_validate}",
                context,
            )
        ]
    return []
