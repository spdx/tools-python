#  SPDX-FileCopyrightText: 2023 spdx contributors
#
#  SPDX-License-Identifier: Apache-2.0
from dataclasses import field
from datetime import datetime
from enum import Enum, auto
from typing import Dict, List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model import CreationInformation, ExternalIdentifier, ExternalReference, IntegrityMethod
from spdx_tools.spdx3.model.software import Package, SoftwarePurpose


class ConfidentialityLevelType(Enum):
    RED = auto()
    AMBER = auto()
    GREEN = auto()
    CLEAR = auto()


class DatasetAvailabilityType(Enum):
    DIRECT_DOWNLOAD = auto()
    SCRAPING_SCRIPT = auto()
    QUERY = auto()
    CLICKTHROUGH = auto()
    REGISTRATION = auto()


@dataclass_with_properties
class Dataset(Package):
    data_collection_process: Optional[str] = None
    intended_use: Optional[str] = None
    dataset_size: Optional[int] = None
    dataset_noise: Optional[str] = None
    data_preprocessing: Optional[str] = None
    sensor: Dict[str, Optional[str]] = field(default_factory=dict)
    known_bias: Optional[str] = None
    sensitive_personal_information: Optional[bool] = None
    anonymization_method_used: List[str] = field(default_factory=list)
    confidentiality_level: Optional[ConfidentialityLevelType] = None
    dataset_update_mechanism: Optional[str] = None
    dataset_availability: Optional[DatasetAvailabilityType] = None

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
        data_collection_process: Optional[str] = None,
        intended_use: Optional[str] = None,
        dataset_size: Optional[int] = None,
        dataset_noise: Optional[str] = None,
        data_preprocessing: Optional[str] = None,
        sensor: Dict[str, Optional[str]] = None,
        known_bias: Optional[str] = None,
        sensitive_personal_information: Optional[bool] = None,
        anonymization_method_used: List[str] = None,
        confidentiality_level: Optional[ConfidentialityLevelType] = None,
        dataset_update_mechanism: Optional[str] = None,
        dataset_availability: Optional[DatasetAvailabilityType] = None,
    ):
        verified_using = [] if verified_using is None else verified_using
        external_references = [] if external_references is None else external_references
        external_identifier = [] if external_identifier is None else external_identifier
        package_purpose = [] if package_purpose is None else package_purpose
        sensors = {} if sensor is None else sensor
        anonymization_method_used = [] if anonymization_method_used is None else anonymization_method_used
        check_types_and_set_values(self, locals())
