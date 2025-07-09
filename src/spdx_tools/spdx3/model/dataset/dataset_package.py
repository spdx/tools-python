# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from dataclasses import field
from datetime import datetime
from enum import Enum, auto

from beartype.typing import Dict, List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values

from ..core.creation_info import CreationInfo
from ..core.external_identifier import ExternalIdentifier
from ..core.external_ref import ExternalRef
from ..core.integrity_method import IntegrityMethod
from ..licensing.license_field import LicenseField
from ..software.package import Package
from ..software.software_purpose import SoftwarePurpose


class DatasetType(Enum):
    AUDIO = auto()
    CATEGORICAL = auto()
    GRAPH = auto()
    IMAGE = auto()
    NO_ASSERTION = auto()
    NUMERIC = auto()
    OTHER = auto()
    SENSOR = auto()
    STRUCTURED = auto()
    SYNTACTIC = auto()
    TEXT = auto()
    TIMESERIES = auto()
    TIMESTAMP = auto()
    VIDEO = auto()


class ConfidentialityLevelType(Enum):
    RED = auto()
    AMBER = auto()
    GREEN = auto()
    CLEAR = auto()


class DatasetAvailabilityType(Enum):
    CLICKTHROUGH = auto()
    DIRECT_DOWNLOAD = auto()
    QUERY = auto()
    REGISTRATION = auto()
    SCRAPING_SCRIPT = auto()


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
    has_sensitive_personal_information: Optional[bool] = None
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
        verified_using: List[IntegrityMethod] = [],
        external_ref: List[ExternalRef] = [],
        external_identifier: List[ExternalIdentifier] = [],
        extension: Optional[str] = None,
        supplied_by: List[str] = [],
        valid_until_time: Optional[datetime] = None,
        standard: List[str] = [],
        content_identifier: Optional[str] = None,
        additional_purpose: List[SoftwarePurpose] = [],
        concluded_license: Optional[LicenseField] = None,
        declared_license: Optional[LicenseField] = None,
        copyright_text: Optional[str] = None,
        attribution_text: Optional[str] = None,
        package_version: Optional[str] = None,
        package_url: Optional[str] = None,
        home_page: Optional[str] = None,
        source_info: Optional[str] = None,
        data_collection_process: Optional[str] = None,
        intended_use: Optional[str] = None,
        dataset_size: Optional[int] = None,
        dataset_noise: Optional[str] = None,
        data_preprocessing: List[str] = [],
        sensor: Dict[str, Optional[str]] = {},
        known_bias: List[str] = [],
        has_sensitive_personal_information: Optional[bool] = None,
        anonymization_method_used: List[str] = [],
        confidentiality_level: Optional[ConfidentialityLevelType] = None,
        dataset_update_mechanism: Optional[str] = None,
        dataset_availability: Optional[DatasetAvailabilityType] = None,
    ):
        verified_using = [] if not verified_using else verified_using
        external_ref = [] if not external_ref else external_ref
        external_identifier = [] if not external_identifier else external_identifier
        originated_by = [] if not originated_by else originated_by
        additional_purpose = [] if not additional_purpose else additional_purpose
        supplied_by = [] if not supplied_by else supplied_by
        standard = [] if not standard else standard
        data_preprocessing = [] if not data_preprocessing else data_preprocessing
        sensor = {} if not sensor else sensor
        known_bias = [] if not known_bias else known_bias
        anonymization_method_used = (
            [] if not anonymization_method_used else anonymization_method_used
        )
        check_types_and_set_values(self, locals())
