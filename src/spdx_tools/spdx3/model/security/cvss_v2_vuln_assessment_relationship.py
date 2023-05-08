# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime
from typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model import (
    Agent,
    CreationInformation,
    Element,
    ExternalIdentifier,
    ExternalReference,
    IntegrityMethod,
)
from spdx_tools.spdx3.model.security.vuln_assessment_relationship import VulnAssessmentRelationship


@dataclass_with_properties
class CvssV2VulnAssessmentRelationship(VulnAssessmentRelationship):
    score: float
    severity: Optional[str] = None
    vector: Optional[str] = None

    def __init__(
        self,
        spdx_id: str,
        creation_info: CreationInformation,
        score: float,
        name: Optional[str] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        comment: Optional[str] = None,
        verified_using: List[IntegrityMethod] = None,
        external_references: List[ExternalReference] = None,
        external_identifier: List[ExternalIdentifier] = None,
        extension: None = None,
        assessed_element: Optional[Element] = None,
        published_time: Optional[datetime] = None,
        supplied_by: Optional[Agent] = None,
        modified_time: Optional[datetime] = None,
        withdrawn_time: Optional[datetime] = None,
        severity: Optional[str] = None,
        vector: Optional[str] = None,
    ):
        verified_using = [] if verified_using is None else verified_using
        external_references = [] if external_references is None else external_references
        external_identifier = [] if external_identifier is None else external_identifier
        check_types_and_set_values(self, locals())
