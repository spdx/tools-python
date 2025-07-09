# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from .cvss_v2_vuln_assessment_relationship import CvssV2VulnAssessmentRelationship
from .cvss_v3_vuln_assessment_relationship import CvssV3VulnAssessmentRelationship
from .epss_vuln_assessment_relationship import EpssVulnAssessmentRelationship
from .exploit_catalog_vuln_assessment_relationship import (
    ExploitCatalogType,
    ExploitCatalogVulnAssessmentRelationship,
)
from .ssvc_vuln_assessment_relationship import (
    SsvcDecisionType,
    SsvcVulnAssessmentRelationship,
)
from .vex_affected_vuln_assessment_relationship import (
    VexAffectedVulnAssessmentRelationship,
)
from .vex_fixed_vuln_assessment_relationship import VexFixedVulnAssessmentRelationship
from .vex_not_affected_vuln_assessment_relationship import (
    VexNotAffectedVulnAssessmentRelationship,
    VexJustificationType,
)
from .vex_under_investigation_vuln_assessment_relationship import (
    VexUnderInvestigationVulnAssessmentRelationship,
)
from .vex_vuln_assessment_relationship import VexVulnAssessmentRelationship
from .vuln_assessment_relationship import VulnAssessmentRelationship
from .vulnerability import Vulnerability

__all__ = [
    "CvssV2VulnAssessmentRelationship",
    "CvssV3VulnAssessmentRelationship",
    "EpssVulnAssessmentRelationship",
    "ExploitCatalogType",
    "ExploitCatalogVulnAssessmentRelationship",
    "SsvcDecisionType",
    "SsvcVulnAssessmentRelationship",
    "VexAffectedVulnAssessmentRelationship",
    "VexFixedVulnAssessmentRelationship",
    "VexNotAffectedVulnAssessmentRelationship",
    "VexJustificationType",
    "VexUnderInvestigationVulnAssessmentRelationship",
    "VexVulnAssessmentRelationship",
    "VulnAssessmentRelationship",
    "Vulnerability",
]
