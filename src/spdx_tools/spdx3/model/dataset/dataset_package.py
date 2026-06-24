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
from spdx_tools.spdx3.model.artifact import SupportType
from spdx_tools.spdx3.model.extension.extension import Extension
from spdx_tools.spdx3.model.presence_type import PresenceType
from spdx_tools.spdx3.model.software import Package, SoftwarePurpose
from spdx_tools.spdx3.model.software.content_identifier import ContentIdentifier


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
class DatasetPackage(Package):
    dataset_type: List[DatasetType] = field(default_factory=list)
    data_collection_process: Optional[str] = None
    intended_use: Optional[str] = None
    dataset_size: Optional[int] = None
    dataset_noise: Optional[str] = None
    data_preprocessing: List[str] = field(default_factory=list)
    sensor: Dict[str, Optional[str]] = field(default_factory=dict)
    known_bias: List[str] = field(default_factory=list)
    has_sensitive_personal_information: Optional[PresenceType] = None
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
        creation_info: CreationInfo,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        comment: Optional[str] = None,
        verified_using: List[IntegrityMethod] | None = None,
        external_reference: List[ExternalReference] | None = None,
        external_identifier: List[ExternalIdentifier] | None = None,
        extension: List[Extension] | None = None,
        supplied_by: Optional[str] = None,
        valid_until_time: Optional[datetime] = None,
        standard: List[str] | None = None,
        content_identifier: List[ContentIdentifier] | None = None,
        additional_purpose: List[SoftwarePurpose] | None = None,
        copyright_text: Optional[str] = None,
        attribution_text: List[str] | None = None,
        package_version: Optional[str] = None,
        package_url: Optional[str] = None,
        home_page: Optional[str] = None,
        source_info: Optional[str] = None,
        data_collection_process: Optional[str] = None,
        intended_use: Optional[str] = None,
        dataset_size: Optional[int] = None,
        dataset_noise: Optional[str] = None,
        data_preprocessing: List[str] | None = None,
        sensor: Dict[str, Optional[str]] | None = None,
        known_bias: List[str] | None = None,
        has_sensitive_personal_information: Optional[PresenceType] = None,
        anonymization_method_used: List[str] | None = None,
        confidentiality_level: Optional[ConfidentialityLevelType] = None,
        dataset_update_mechanism: Optional[str] = None,
        dataset_availability: Optional[DatasetAvailabilityType] = None,
        standard_name: List[str] | None = None,
        support_level: List[SupportType] | None = None,
    ):
        verified_using = [] if verified_using is None else verified_using
        external_reference = [] if external_reference is None else external_reference
        external_identifier = [] if external_identifier is None else external_identifier
        extension = [] if extension is None else extension
        originated_by = [] if originated_by is None else originated_by
        additional_purpose = [] if additional_purpose is None else additional_purpose
        attribution_text = [] if attribution_text is None else attribution_text
        standard = [] if standard is None else standard
        content_identifier = [] if content_identifier is None else content_identifier
        data_preprocessing = [] if data_preprocessing is None else data_preprocessing
        sensor = {} if sensor is None else sensor
        known_bias = [] if known_bias is None else known_bias
        anonymization_method_used = [] if anonymization_method_used is None else anonymization_method_used
        standard_name = [] if standard_name is None else standard_name
        support_level = [] if support_level is None else support_level
        check_types_and_set_values(self, locals())
