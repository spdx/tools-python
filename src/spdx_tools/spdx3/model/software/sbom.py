# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from dataclasses import field
from enum import Enum, auto

from beartype.typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model import (
    Bom,
    CreationInfo,
    ExternalIdentifier,
    ExternalReference,
    IntegrityMethod,
    ProfileIdentifierType,
)
from spdx_tools.spdx3.model.extension.extension import Extension


class SbomType(Enum):
    DESIGN = auto()
    SOURCE = auto()
    BUILD = auto()
    DEPLOYED = auto()
    RUNTIME = auto()
    ANALYZED = auto()


@dataclass_with_properties
class Sbom(Bom):
    sbom_type: List[SbomType] = field(default_factory=list)

    # We overwrite the super-__init__ as check_types_and_set_values()
    # takes care of all fields (including inherited ones).
    def __init__(
        self,
        spdx_id: str,
        element: List[str],
        root_element: List[str],
        creation_info: CreationInfo,
        name: Optional[str] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        comment: Optional[str] = None,
        verified_using: List[IntegrityMethod] | None = None,
        external_reference: List[ExternalReference] | None = None,
        external_identifier: List[ExternalIdentifier] | None = None,
        extension: List[Extension] | None = None,
        context: Optional[str] = None,
        sbom_type: List[SbomType] | None = None,
        profile_conformance: List[ProfileIdentifierType] | None = None,
    ):
        verified_using = [] if verified_using is None else verified_using
        external_reference = [] if external_reference is None else external_reference
        external_identifier = [] if external_identifier is None else external_identifier
        sbom_type = [] if sbom_type is None else sbom_type
        profile_conformance = [] if profile_conformance is None else profile_conformance
        extension = [] if extension is None else extension
        check_types_and_set_values(self, locals())
