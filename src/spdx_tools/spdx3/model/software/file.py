# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model.artifact import Artifact
from spdx_tools.spdx3.model.creation_information import CreationInformation
from spdx_tools.spdx3.model.external_identifier import ExternalIdentifier
from spdx_tools.spdx3.model.external_reference import ExternalReference
from spdx_tools.spdx3.model.integrity_method import IntegrityMethod
from spdx_tools.spdx3.model.software.software_purpose import SoftwarePurpose


@dataclass_with_properties
class File(Artifact):
    content_identifier: Optional[str] = None  # should be a valid URI
    file_purpose: Optional[List[SoftwarePurpose]] = None
    content_type: Optional[str] = None  # placeholder for MediaType

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
        file_purpose: Optional[List[SoftwarePurpose]] = None,
        content_type: Optional[str] = None,
    ):
        verified_using = [] if verified_using is None else verified_using
        external_references = [] if external_references is None else external_references
        external_identifier = [] if external_identifier is None else external_identifier
        file_purpose = [] if file_purpose is None else file_purpose
        check_types_and_set_values(self, locals())
