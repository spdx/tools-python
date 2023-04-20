# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from dataclasses import field
from datetime import datetime
from enum import Enum, auto
from typing import Dict, List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model import CreationInformation, ExternalIdentifier, ExternalReference, IntegrityMethod
from spdx_tools.spdx3.model.software import Package, SoftwarePurpose


class SafetyRiskAssessmentType(Enum):
    SERIOUS = auto()
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()


@dataclass_with_properties
class AIPackage(Package):
    energy_consumption: Optional[str] = None
    standards_compliance: List[str] = field(default_factory=list)
    limitations: Optional[str] = None
    type_of_model: List[str] = field(default_factory=list)
    information_about_training: Optional[str] = None
    information_about_application: Optional[str] = None
    hyperparameters: Dict[str, Optional[str]] = field(default_factory=dict)
    data_preprocessing_steps: Optional[str] = None
    model_explainability_mechanisms: Optional[str] = None
    sensitive_personal_information: Optional[bool] = None
    metrics_decision_thresholds: Dict[str, Optional[str]] = field(default_factory=dict)
    metrics: Dict[str, Optional[str]] = field(default_factory=dict)
    domain: List[str] = field(default_factory=list)
    autonomy_type: Optional[bool] = None
    safety_risk_assessment: Optional[SafetyRiskAssessmentType] = None

    def __init__(
        self,
        spdx_id: str,
        creation_info: CreationInformation,
        name: Optional[str] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        comment: Optional[str] = None,
        verified_using: List[IntegrityMethod] = None,
        external_references: List[ExternalReference] = None,
        external_identifier: List[ExternalIdentifier] = None,
        extension: None = None,
        originated_by: Optional[str] = None,
        content_identifier: Optional[str] = None,
        built_time: Optional[datetime] = None,
        release_time: Optional[datetime] = None,
        valid_until_time: Optional[datetime] = None,
        package_purpose: List[SoftwarePurpose] = None,
        package_version: Optional[str] = None,
        download_location: Optional[str] = None,
        package_url: Optional[str] = None,
        homepage: Optional[str] = None,
        source_info: Optional[str] = None,
        energy_consumption: Optional[str] = None,
        standards_compliance: List[str] = None,
        limitations: Optional[str] = None,
        type_of_model: List[str] = None,
        information_about_training: Optional[str] = None,
        information_about_application: Optional[str] = None,
        hyperparameters: Dict[str, Optional[str]] = None,
        data_preprocessing_steps: Optional[str] = None,
        model_explainability_mechanisms: Optional[str] = None,
        sensitive_personal_information: Optional[bool] = None,
        metrics_decision_thresholds: Dict[str, Optional[str]] = None,
        metrics: Dict[str, Optional[str]] = None,
        domain: List[str] = None,
        autonomy_type: Optional[bool] = None,
        safety_risk_assessment: Optional[SafetyRiskAssessmentType] = None,
    ):
        verified_using = [] if verified_using is None else verified_using
        external_references = [] if external_references is None else external_references
        external_identifier = [] if external_identifier is None else external_identifier
        package_purpose = [] if package_purpose is None else package_purpose
        standards_compliance = [] if standards_compliance is None else standards_compliance
        type_of_model = [] if type_of_model is None else type_of_model
        hyperparameters = {} if hyperparameters is None else hyperparameters
        metrics_decision_thresholds = {} if metrics_decision_thresholds is None else metrics_decision_thresholds
        metrics = {} if metrics is None else metrics
        domain = [] if domain is None else domain
        check_types_and_set_values(self, locals())
