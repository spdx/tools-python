# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from dataclasses import field
from datetime import datetime
from enum import Enum, auto

from beartype.typing import Dict, List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model.core import (
    CreationInfo,
    ExternalIdentifier,
    ExternalReference,
    IntegrityMethod,
)
from spdx_tools.spdx3.model.licensing import LicenseField
from spdx_tools.spdx3.model.software import Package, SoftwarePurpose


class SafetyRiskAssessmentType(Enum):
    SERIOUS = auto()
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()


@dataclass_with_properties
class AIPackage(Package):
    energy_consumption: Optional[str] = None
    standard_compliance: List[str] = field(default_factory=list)
    limitation: Optional[str] = None
    type_of_model: List[str] = field(default_factory=list)
    information_about_training: Optional[str] = None
    information_about_application: Optional[str] = None
    hyperparameter: Dict[str, Optional[str]] = field(default_factory=dict)
    model_data_preprocessing: List[str] = field(default_factory=list)
    model_explainability: List[str] = field(default_factory=list)
    use_sensitive_personal_information: Optional[bool] = None
    metric_decision_threshold: Dict[str, Optional[str]] = field(default_factory=dict)
    metric: Dict[str, Optional[str]] = field(default_factory=dict)
    domain: List[str] = field(default_factory=list)
    autonomy_type: Optional[bool] = None
    safety_risk_assessment: Optional[SafetyRiskAssessmentType] = None

    def __init__(
        self,
        spdx_id: str,
        name: str,
        supplied_by: List[str],
        download_location: str,
        package_version: str,
        primary_purpose: SoftwarePurpose,
        release_time: datetime,
        creation_info: Optional[CreationInfo] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        comment: Optional[str] = None,
        verified_using: List[IntegrityMethod] = [],
        external_reference: List[ExternalReference] = [],
        external_identifier: List[ExternalIdentifier] = [],
        extension: Optional[str] = None,
        originated_by: List[str] = [],
        built_time: Optional[datetime] = None,
        valid_until_time: Optional[datetime] = None,
        standard: List[str] = [],
        content_identifier: Optional[str] = None,
        additional_purpose: List[SoftwarePurpose] = [],
        concluded_license: Optional[LicenseField] = None,
        declared_license: Optional[LicenseField] = None,
        copyright_text: Optional[str] = None,
        attribution_text: Optional[str] = None,
        package_url: Optional[str] = None,
        homepage: Optional[str] = None,
        source_info: Optional[str] = None,
        energy_consumption: Optional[str] = None,
        standard_compliance: List[str] = [],
        limitation: Optional[str] = None,
        type_of_model: List[str] = [],
        information_about_training: Optional[str] = None,
        information_about_application: Optional[str] = None,
        hyperparameter: Dict[str, Optional[str]] = {},
        model_data_preprocessing: List[str] = [],
        model_explainability: List[str] = [],
        use_sensitive_personal_information: Optional[bool] = None,
        metric_decision_threshold: Dict[str, Optional[str]] = {},
        metric: Dict[str, Optional[str]] = {},
        domain: List[str] = [],
        autonomy_type: Optional[bool] = None,
        safety_risk_assessment: Optional[SafetyRiskAssessmentType] = None,
    ):
        verified_using = [] if not verified_using else verified_using
        external_reference = [] if not external_reference else external_reference
        external_identifier = [] if not external_identifier else external_identifier
        originated_by = [] if not originated_by else originated_by
        additional_purpose = [] if not additional_purpose else additional_purpose
        standard = [] if not standard else standard
        standard_compliance = [] if not standard_compliance else standard_compliance
        type_of_model = [] if not type_of_model else type_of_model
        hyperparameter = {} if not hyperparameter else hyperparameter
        model_data_preprocessing = [] if not model_data_preprocessing else model_data_preprocessing
        model_explainability = [] if not model_explainability else model_explainability
        metric_decision_threshold = {} if not metric_decision_threshold else metric_decision_threshold
        metric = {} if not metric else metric
        domain = [] if not not domain else domain
        check_types_and_set_values(self, locals())
