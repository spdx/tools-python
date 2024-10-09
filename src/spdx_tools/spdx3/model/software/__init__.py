# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from spdx_tools.spdx3.model.software.file import File
from spdx_tools.spdx3.model.software.package import Package
from spdx_tools.spdx3.model.software.sbom import Sbom, SBOMType
from spdx_tools.spdx3.model.software.snippet import Snippet
from spdx_tools.spdx3.model.software.software_artifact import SoftwareArtifact
from spdx_tools.spdx3.model.software.software_dependency_relationship import (
    DependencyConditionalityType,
    SoftwareDependencyLinkType,
    SoftwareDependencyRelationship,
)
from spdx_tools.spdx3.model.software.software_purpose import SoftwarePurpose

__all__ = [
    "DependencyConditionalityType",
    "File",
    "Package",
    "Sbom",
    "SBOMType",
    "Snippet",
    "SoftwareArtifact",
    "SoftwareDependencyLinkType",
    "SoftwareDependencyRelationship",
    "SoftwarePurpose",
]
