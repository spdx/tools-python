# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from dataclasses import field
from enum import Enum, auto

from beartype.typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model.core import (
    Bom,
    CreationInfo,
    ExternalIdentifier,
    ExternalMap,
    ExternalRef,
    IntegrityMethod,
    NamespaceMap,
)


class SBOMType(Enum):
    DESIGN = auto()
    SOURCE = auto()
    BUILD = auto()
    DEPLOYED = auto()
    RUNTIME = auto()
    ANALYZED = auto()


@dataclass_with_properties
class Sbom(Bom):
    sbom_type: List[SBOMType] = field(default_factory=list)

    # We overwrite the super-__init__ as check_types_and_set_values()
    # takes care of all fields (including inherited ones).
    def __init__(
        self,
        spdx_id: str,
        element: List[str],
        root_element: List[str],
        creation_info: Optional[CreationInfo] = None,
        name: Optional[str] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        comment: Optional[str] = None,
        verified_using: List[IntegrityMethod] = [],
        external_ref: List[ExternalRef] = [],
        external_identifier: List[ExternalIdentifier] = [],
        extension: Optional[str] = None,
        namespace: List[NamespaceMap] = [],
        import_: List[ExternalMap] = [],
        context: Optional[str] = None,
        sbom_type: List[SBOMType] = [],
    ):
        verified_using = [] if not verified_using else verified_using
        external_ref = [] if not external_ref else external_ref
        external_identifier = [] if not external_identifier else external_identifier
        namespace = [] if not namespace else namespace
        import_ = [] if not import_ else import_
        sbom_type = [] if not sbom_type else sbom_type
        check_types_and_set_values(self, locals())
