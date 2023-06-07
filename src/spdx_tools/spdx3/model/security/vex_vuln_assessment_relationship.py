# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from abc import abstractmethod

from beartype.typing import Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.spdx3.model.security.vuln_assessment_relationship import VulnAssessmentRelationship


@dataclass_with_properties
class VexVulnAssessmentRelationship(VulnAssessmentRelationship):
    vex_version: Optional[str] = None
    status_notes: Optional[str] = None

    @abstractmethod
    def __init__(self):
        pass
