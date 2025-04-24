# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from abc import abstractmethod
from dataclasses import field

from beartype.typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties

from ..core.artifact import Artifact
from ..licensing.license_field import LicenseField
from .software_purpose import SoftwarePurpose


@dataclass_with_properties
class SoftwareArtifact(Artifact):
    content_identifier: Optional[str] = None
    primary_purpose: Optional[SoftwarePurpose] = None
    additional_purpose: List[SoftwarePurpose] = field(default_factory=list)
    concluded_license: Optional[LicenseField] = None
    declared_license: Optional[LicenseField] = None
    copyright_text: Optional[str] = None
    attribution_text: Optional[str] = None

    @abstractmethod
    def __init__(self):
        pass
