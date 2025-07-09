# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from dataclasses import field
from enum import Enum, auto

from beartype.typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values


class ExternalRefType(Enum):
    ALT_DOWNLOAD_LOCATION = auto()
    ALT_WEB_PAGE = auto()
    BINARY_ARTIFACT = auto()
    BOWER = auto()
    BUILD_META = auto()
    BUILD_SYSTEM = auto()
    CERTIFICATION_REPORT = auto()
    CHAT = auto()
    COMPONENT_ANALYSIS_REPORT = auto()
    CWE = auto()
    DOCUMENTATION = auto()
    DYNAMIC_ANALYSIS_REPORT = auto()
    EOL_NOTICE = auto()
    FUNDING = auto()
    ISSUE_TRACKER = auto()
    LICENSE = auto()
    MAILING_LIST = auto()
    MAVEN_CENTRAL = auto()
    METRICS = auto()
    NPM = auto()
    NUGET = auto()
    OTHER = auto()
    PRIVACY_ASSESSMENT = auto()
    PRODUCT_METADATA = auto()
    PURCHASES_ORDER = auto()
    QUALITY_ASSESSMENT_REPORT = auto()
    RELEASE_HISTORY = auto()
    RELEASE_NOTES = auto()
    RISK_ASSESSMENT = auto()
    RUNTIME_ANALYSIS_REPORT = auto()
    SECURE_SOFTWARE_ATTESTATION = auto()
    SECURITY_ADVERSARY_MODEL = auto()
    SECURITY_ADVISORY = auto()
    SECURITY_FIX = auto()
    SECURITY_OTHER = auto()
    SECURITY_PEN_TEST_REPORT = auto()
    SECURITY_POLICY = auto()
    SECURITY_THREAT_MODEL = auto()
    SOCIAL_MEDIA = auto()
    SOURCE_ARTIFACT = auto()
    STATIC_ANALYSIS_REPORT = auto()
    SUPPORT = auto()
    VCS = auto()
    VULNERABILITY_DISCLOSURE_REPORT = auto()
    VULNERABILITY_EXPLOITABILITY_ASSESSMENT = auto()


@dataclass_with_properties
class ExternalRef:
    external_ref_type: Optional[ExternalRefType] = None
    locator: List[str] = field(default_factory=list)
    content_type: Optional[str] = None  # placeholder for MediaType
    comment: Optional[str] = None

    def __init__(
        self,
        external_ref_type: Optional[ExternalRefType] = None,
        locator: List[str] = [],
        content_type: Optional[str] = None,
        comment: Optional[str] = None,
    ):
        locator = [] if not locator else locator
        check_types_and_set_values(self, locals())
