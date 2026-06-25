# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from dataclasses import field

from beartype.typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model import (
    CreationInfo,
    ExternalIdentifier,
    ExternalMap,
    ExternalReference,
    IntegrityMethod,
    NamespaceMap,
    ProfileIdentifierType,
)
from spdx_tools.spdx3.model.element_collection import ElementCollection
from spdx_tools.spdx3.model.extension.extension import Extension


@dataclass_with_properties
class SpdxDocument(ElementCollection):
    namespace_map: List[NamespaceMap] = field(default_factory=list)
    imports: List[ExternalMap] = field(default_factory=list)
    data_license: Optional[str] = None

    # The inherited field "name" is required for a SpdxDocument, no longer optional.
    # We overwrite the super-__init__ as check_types_and_set_values()
    # takes care of all fields (including inherited ones).
    def __init__(
        self,
        spdx_id: str,
        name: str,
        element: List[str],
        root_element: List[str],
        creation_info: CreationInfo,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        comment: Optional[str] = None,
        verified_using: List[IntegrityMethod] | None = None,
        external_reference: List[ExternalReference] | None = None,
        external_identifier: List[ExternalIdentifier] | None = None,
        extension: List[Extension] | None = None,
        namespace_map: List[NamespaceMap] | None = None,
        profile_conformance: List[ProfileIdentifierType] | None = None,
        imports: List[ExternalMap] | None = None,
        data_license: Optional[str] = None,
    ):
        verified_using = [] if verified_using is None else verified_using
        external_reference = [] if external_reference is None else external_reference
        external_identifier = [] if external_identifier is None else external_identifier
        extension = [] if extension is None else extension
        namespace_map = [] if namespace_map is None else namespace_map
        profile_conformance = [] if profile_conformance is None else profile_conformance
        imports = [] if imports is None else imports
        check_types_and_set_values(self, locals())
