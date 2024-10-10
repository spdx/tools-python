# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from .file import File
from .package import Package
from .sbom import Sbom, SBOMType
from .snippet import Snippet
from .software_artifact import SoftwareArtifact
from .software_dependency_relationship import (
    DependencyConditionalityType,
    SoftwareDependencyLinkType,
    SoftwareDependencyRelationship,
)
from .software_purpose import SoftwarePurpose

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
