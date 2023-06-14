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


class DatasetType(Enum):
    STRUCTURED = auto()
    NUMERIC = auto()
    TEXT = auto()
    CATEGORICAL = auto()
    GRAPH = auto()
    TIMESERIES = auto()
    TIMESTAMP = auto()
    SENSOR = auto()
    IMAGE = auto()
    SYNTACTIC = auto()
    AUDIO = auto()
    VIDEO = auto()
    OTHER = auto()
    NO_ASSERTION = auto()


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
    dataset_type: List[DatasetType] = None
    data_collection_process: Optional[str] = None
    intended_use: Optional[str] = None
    dataset_size: Optional[int] = None
    dataset_noise: Optional[str] = None
    data_preprocessing: List[str] = field(default_factory=list)
    sensor: Dict[str, Optional[str]] = field(default_factory=dict)
    known_bias: List[str] = field(default_factory=list)
    sensitive_personal_information: Optional[bool] = None
    anonymization_method_used: List[str] = field(default_factory=list)
    confidentiality_level: Optional[ConfidentialityLevelType] = None
    dataset_update_mechanism: Optional[str] = None
    dataset_availability: Optional[DatasetAvailabilityType] = None

    def __init__(
        self,
        spdx_id: str,
        name: str,
        originated_by: List[str],
        download_location: str,
        primary_purpose: SoftwarePurpose,
        built_time: datetime,
        release_time: datetime,
        dataset_type: List[DatasetType],
        creation_info: Optional[CreationInfo] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        comment: Optional[str] = None,
        verified_using: List[IntegrityMethod] = None,
        external_reference: List[ExternalReference] = None,
        external_identifier: List[ExternalIdentifier] = None,
        extension: Optional[str] = None,
        supplied_by: List[str] = None,
        valid_until_time: Optional[datetime] = None,
        standard: List[str] = None,
        content_identifier: Optional[str] = None,
        additional_purpose: List[SoftwarePurpose] = None,
        concluded_license: Optional[LicenseField] = None,
        declared_license: Optional[LicenseField] = None,
        copyright_text: Optional[str] = None,
        attribution_text: Optional[str] = None,
        package_version: Optional[str] = None,
        package_url: Optional[str] = None,
        homepage: Optional[str] = None,
        source_info: Optional[str] = None,
        data_collection_process: Optional[str] = None,
        intended_use: Optional[str] = None,
        dataset_size: Optional[int] = None,
        dataset_noise: Optional[str] = None,
        data_preprocessing: List[str] = None,
        sensor: Dict[str, Optional[str]] = None,
        known_bias: List[str] = None,
        sensitive_personal_information: Optional[bool] = None,
        anonymization_method_used: List[str] = None,
        confidentiality_level: Optional[ConfidentialityLevelType] = None,
        dataset_update_mechanism: Optional[str] = None,
        dataset_availability: Optional[DatasetAvailabilityType] = None,
    ):
        verified_using = [] if verified_using is None else verified_using
        external_reference = [] if external_reference is None else external_reference
        external_identifier = [] if external_identifier is None else external_identifier
        originated_by = [] if originated_by is None else originated_by
        additional_purpose = [] if additional_purpose is None else additional_purpose
        supplied_by = [] if supplied_by is None else supplied_by
        standard = [] if standard is None else standard
        data_preprocessing = [] if data_preprocessing is None else data_preprocessing
        sensor = {} if sensor is None else sensor
        known_bias = [] if known_bias is None else known_bias
        anonymization_method_used = [] if anonymization_method_used is None else anonymization_method_used
        check_types_and_set_values(self, locals())
