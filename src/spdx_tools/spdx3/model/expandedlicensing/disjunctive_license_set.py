# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from dataclasses import field
from typing import Optional

from beartype.typing import List

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model.creation_info import CreationInfo
from spdx_tools.spdx3.model.extension.extension import Extension
from spdx_tools.spdx3.model.external_identifier import ExternalIdentifier
from spdx_tools.spdx3.model.external_reference import ExternalReference
from spdx_tools.spdx3.model.integrity_method import IntegrityMethod
from spdx_tools.spdx3.model.simplelicensing.any_license_info import AnyLicenseInfo


@dataclass_with_properties
class DisjunctiveLicenseSet(AnyLicenseInfo):
    member: List[str] = field(default_factory=list)

    def __init__(
        self,
        spdx_id: str,
        member: List[str],
        creation_info: CreationInfo,
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
        member = [] if member is None else member
        check_types_and_set_values(self, locals())
