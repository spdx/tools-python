# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime

from beartype.typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model.core import CreationInfo, ExternalIdentifier, ExternalRef, IntegrityMethod
from spdx_tools.spdx3.model.licensing import LicenseField
from spdx_tools.spdx3.model.software import SoftwareArtifact, SoftwarePurpose


@dataclass_with_properties
class Package(SoftwareArtifact):
    package_version: Optional[str] = None
    download_location: Optional[str] = None  # anyURI
    package_url: Optional[str] = None  # anyURI
    homepage: Optional[str] = None  # anyURI
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
        homepage: Optional[str] = None,
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
