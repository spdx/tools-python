# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime

from beartype.typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values

from ..core.creation_info import CreationInfo
from ..core.external_identifier import ExternalIdentifier
from ..core.external_ref import ExternalRef
from ..core.integrity_method import IntegrityMethod
from ..licensing.license_field import LicenseField
from .software_artifact import SoftwareArtifact
from .software_purpose import SoftwarePurpose


@dataclass_with_properties
class Package(SoftwareArtifact):
    package_version: Optional[str] = None
    download_location: Optional[str] = None  # anyURI
    package_url: Optional[str] = None  # anyURI
    home_page: Optional[str] = None  # anyURI
    source_info: Optional[str] = None

    def __init__(
        self,
        spdx_id: str,
        name: str,
        creation_info: Optional[CreationInfo] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        comment: Optional[str] = None,
        verified_using: List[IntegrityMethod] = [],
        external_ref: List[ExternalRef] = [],
        external_identifier: List[ExternalIdentifier] = [],
        extension: Optional[str] = None,
        originated_by: List[str] = [],
        supplied_by: List[str] = [],
        built_time: Optional[datetime] = None,
        release_time: Optional[datetime] = None,
        valid_until_time: Optional[datetime] = None,
        standard: List[str] = [],
        content_identifier: Optional[str] = None,
        primary_purpose: Optional[SoftwarePurpose] = None,
        additional_purpose: List[SoftwarePurpose] = [],
        concluded_license: Optional[LicenseField] = None,
        declared_license: Optional[LicenseField] = None,
        copyright_text: Optional[str] = None,
        attribution_text: Optional[str] = None,
        package_version: Optional[str] = None,
        download_location: Optional[str] = None,
        package_url: Optional[str] = None,
        home_page: Optional[str] = None,
        source_info: Optional[str] = None,
    ):
        verified_using = [] if not verified_using else verified_using
        external_ref = [] if not external_ref else external_ref
        external_identifier = [] if not external_identifier else external_identifier
        originated_by = [] if not originated_by else originated_by
        supplied_by = [] if not supplied_by else supplied_by
        standard = [] if not standard else standard
        additional_purpose = [] if not additional_purpose else additional_purpose
        check_types_and_set_values(self, locals())
