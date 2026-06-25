# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model.creation_info import CreationInfo
from spdx_tools.spdx3.model.expandedlicensing.license_addition import LicenseAddition
from spdx_tools.spdx3.model.extension.extension import Extension
from spdx_tools.spdx3.model.external_identifier import ExternalIdentifier
from spdx_tools.spdx3.model.external_reference import ExternalReference
from spdx_tools.spdx3.model.integrity_method import IntegrityMethod


@dataclass_with_properties
class CustomLicenseAddition(LicenseAddition):
    def __init__(
        self,
        spdx_id: str,
        addition_text: str,
        creation_info: CreationInfo,
        name: Optional[str] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        comment: Optional[str] = None,
        verified_using: List[IntegrityMethod] | None = None,
        external_reference: List[ExternalReference] | None = None,
        external_identifier: List[ExternalIdentifier] | None = None,
        extension: List[Extension] | None = None,
        is_deprecated_addition_id: Optional[bool] = None,
        license_xml: Optional[str] = None,
        obsoleted_by: Optional[str] = None,
        see_also: List[str] | None = None,
        standard_addition_template: Optional[str] = None,
    ):
        verified_using = [] if verified_using is None else verified_using
        external_reference = [] if external_reference is None else external_reference
        external_identifier = [] if external_identifier is None else external_identifier
        extension = [] if extension is None else extension
        see_also = [] if see_also is None else see_also
        check_types_and_set_values(self, locals())
