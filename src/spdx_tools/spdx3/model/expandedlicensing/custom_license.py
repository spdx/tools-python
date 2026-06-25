# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model.creation_info import CreationInfo
from spdx_tools.spdx3.model.expandedlicensing.license import License
from spdx_tools.spdx3.model.extension.extension import Extension
from spdx_tools.spdx3.model.external_identifier import ExternalIdentifier
from spdx_tools.spdx3.model.external_reference import ExternalReference
from spdx_tools.spdx3.model.integrity_method import IntegrityMethod


@dataclass_with_properties
class CustomLicense(License):
    def __init__(
        self,
        spdx_id: str,
        license_text: str,
        creation_info: CreationInfo,
        see_also: List[str] | None = None,
        is_osi_approved: Optional[bool] = None,
        is_fsf_libre: Optional[bool] = None,
        standard_license_header: Optional[str] = None,
        standard_license_template: Optional[str] = None,
        is_deprecated_license_id: Optional[bool] = None,
        obsoleted_by: Optional[str] = None,
        license_xml: Optional[str] = None,
        name: Optional[str] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        comment: Optional[str] = None,
        verified_using: List[IntegrityMethod] | None = None,
        external_reference: List[ExternalReference] | None = None,
        external_identifier: List[ExternalIdentifier] | None = None,
        extension: List[Extension] | None = None,
    ):
        verified_using = [] if verified_using is None else verified_using
        external_reference = [] if external_reference is None else external_reference
        external_identifier = [] if external_identifier is None else external_identifier
        extension = [] if extension is None else extension
        see_also = [] if see_also is None else see_also
        check_types_and_set_values(self, locals())
