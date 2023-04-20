# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime
from typing import List, Optional, Tuple

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model import (
    Artifact,
    CreationInformation,
    ExternalIdentifier,
    ExternalReference,
    IntegrityMethod,
)
from spdx_tools.spdx3.model.software import SoftwarePurpose


@dataclass_with_properties
class Snippet(Artifact):
    content_identifier: Optional[str] = None  # anyURI
    snippet_purpose: Optional[List[SoftwarePurpose]] = None
    byte_range: Optional[Tuple[int, int]] = None
    line_range: Optional[Tuple[int, int]] = None

    def __init__(
        self,
        spdx_id: str,
        creation_info: CreationInformation,
        name: Optional[str] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        comment: Optional[str] = None,
        verified_using: Optional[List[IntegrityMethod]] = None,
        external_references: Optional[List[ExternalReference]] = None,
        external_identifier: Optional[List[ExternalIdentifier]] = None,
        extension: None = None,
        originated_by: Optional[str] = None,
        content_identifier: Optional[str] = None,
        built_time: Optional[datetime] = None,
        release_time: Optional[datetime] = None,
        valid_until_time: Optional[datetime] = None,
        snippet_purpose: Optional[List[SoftwarePurpose]] = None,
        byte_range: Optional[Tuple[int, int]] = None,
        line_range: Optional[Tuple[int, int]] = None,
    ):
        verified_using = [] if verified_using is None else verified_using
        external_references = [] if external_references is None else external_references
        external_identifier = [] if external_identifier is None else external_identifier
        snippet_purpose = [] if snippet_purpose is None else snippet_purpose
        check_types_and_set_values(self, locals())