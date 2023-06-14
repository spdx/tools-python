# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from dataclasses import field
from datetime import datetime
from enum import Enum, auto

from beartype.typing import Dict, List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model import CreationInfo, ExternalIdentifier, ExternalReference, IntegrityMethod
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
    sensitive_personal_information: Optional[bool] = None
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
        verified_using: List[IntegrityMethod] = None,
        external_reference: List[ExternalReference] = None,
        external_identifier: List[ExternalIdentifier] = None,
        extension: Optional[str] = None,
        originated_by: List[str] = None,
        built_time: Optional[datetime] = None,
        valid_until_time: Optional[datetime] = None,
        standard: List[str] = None,
        content_identifier: Optional[str] = None,
        additional_purpose: List[SoftwarePurpose] = None,
        concluded_license: Optional[LicenseField] = None,
        declared_license: Optional[LicenseField] = None,
        copyright_text: Optional[str] = None,
        attribution_text: Optional[str] = None,
        package_url: Optional[str] = None,
        homepage: Optional[str] = None,
        source_info: Optional[str] = None,
        energy_consumption: Optional[str] = None,
        standard_compliance: List[str] = None,
        limitation: Optional[str] = None,
        type_of_model: List[str] = None,
        information_about_training: Optional[str] = None,
        information_about_application: Optional[str] = None,
        hyperparameter: Dict[str, Optional[str]] = None,
        model_data_preprocessing: List[str] = None,
        model_explainability: List[str] = None,
        sensitive_personal_information: Optional[bool] = None,
        metric_decision_threshold: Dict[str, Optional[str]] = None,
        metric: Dict[str, Optional[str]] = None,
        domain: List[str] = None,
        autonomy_type: Optional[bool] = None,
        safety_risk_assessment: Optional[SafetyRiskAssessmentType] = None,
    ):
        verified_using = [] if verified_using is None else verified_using
        external_reference = [] if external_reference is None else external_reference
        external_identifier = [] if external_identifier is None else external_identifier
        originated_by = [] if originated_by is None else originated_by
        additional_purpose = [] if additional_purpose is None else additional_purpose
        standard = [] if standard is None else standard
        standard_compliance = [] if standard_compliance is None else standard_compliance
        type_of_model = [] if type_of_model is None else type_of_model
        hyperparameter = {} if hyperparameter is None else hyperparameter
        model_data_preprocessing = [] if model_data_preprocessing is None else model_data_preprocessing
        model_explainability = [] if model_explainability is None else model_explainability
        metric_decision_threshold = {} if metric_decision_threshold is None else metric_decision_threshold
        metric = {} if metric is None else metric
        domain = [] if domain is None else domain
        check_types_and_set_values(self, locals())
