# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime

from beartype.typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model import CreationInfo, ExternalIdentifier, ExternalReference, IntegrityMethod
from spdx_tools.spdx3.model.artifact import SupportType
from spdx_tools.spdx3.model.extension.extension import Extension
from spdx_tools.spdx3.model.software import SoftwarePurpose
from spdx_tools.spdx3.model.software.content_identifier import ContentIdentifier
from spdx_tools.spdx3.model.software.software_artifact import SoftwareArtifact


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
        creation_info: CreationInfo,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        comment: Optional[str] = None,
        verified_using: List[IntegrityMethod] | None = None,
        external_reference: List[ExternalReference] | None = None,
        external_identifier: List[ExternalIdentifier] | None = None,
        extension: List[Extension] | None = None,
        originated_by: List[str] | None = None,
        supplied_by: Optional[str] = None,
        built_time: Optional[datetime] = None,
        release_time: Optional[datetime] = None,
        valid_until_time: Optional[datetime] = None,
        content_identifier: List[ContentIdentifier] | None = None,
        primary_purpose: Optional[SoftwarePurpose] = None,
        additional_purpose: List[SoftwarePurpose] | None = None,
        copyright_text: Optional[str] = None,
        attribution_text: List[str] | None = None,
        package_version: Optional[str] = None,
        download_location: Optional[str] = None,
        package_url: Optional[str] = None,
        home_page: Optional[str] = None,
        source_info: Optional[str] = None,
        standard_name: List[str] | None = None,
        support_level: List[SupportType] | None = None,
    ):
        verified_using = [] if verified_using is None else verified_using
        external_reference = [] if external_reference is None else external_reference
        external_identifier = [] if external_identifier is None else external_identifier
        originated_by = [] if originated_by is None else originated_by
        content_identifier = [] if content_identifier is None else content_identifier
        additional_purpose = [] if additional_purpose is None else additional_purpose
        attribution_text = [] if attribution_text is None else attribution_text
        extension = [] if extension is None else extension
        standard_name = [] if standard_name is None else standard_name
        support_level = [] if support_level is None else support_level
        check_types_and_set_values(self, locals())
