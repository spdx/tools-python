# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model.ai import AIPackage
from spdx_tools.spdx3.model.build import Build
from spdx_tools.spdx3.model.dataset import DatasetPackage
from spdx_tools.spdx3.model.core import (
    Annotation,
    Bom,
    Bundle,
    Organization,
    Person,
    Relationship,
    SoftwareAgent,
    SpdxDocument,
    Tool,
)
from spdx_tools.spdx3.model.software import (
    File,
    Package,
    Sbom,
    Snippet,
    SoftwareDependencyRelationship,
)
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx3.writer.console.ai import write_ai_package
from spdx_tools.spdx3.writer.console.build import write_build
from spdx_tools.spdx3.writer.console.core import (
    write_agent,
    write_annotation,
    write_bom,
    write_bundle,
    write_relationship,
    write_spdx_document,
    write_tool,
)
from spdx_tools.spdx3.writer.console.dataset import (
    write_dataset_package,
)
from spdx_tools.spdx3.writer.console.software import (
    write_file,
    write_package,
    write_sbom,
    write_snippet,
    write_software_dependency_relationship,
)

MAP_CLASS_TO_WRITE_METHOD = {
    AIPackage: write_ai_package,
    Annotation: write_annotation,
    Bom: write_bom,
    Build: write_build,
    Bundle: write_bundle,
    DatasetPackage: write_dataset_package,
    File: write_file,
    Organization: write_agent,
    Package: write_package,
    Person: write_agent,
    Relationship: write_relationship,
    Sbom: write_sbom,
    Snippet: write_snippet,
    SoftwareAgent: write_agent,
    SoftwareDependencyRelationship: write_software_dependency_relationship,
    SpdxDocument: write_spdx_document,
    Tool: write_tool,
}


def write_payload(payload: Payload, text_output: TextIO):
    for element in payload.get_full_map().values():
        write_method = MAP_CLASS_TO_WRITE_METHOD[type(element)]
        write_method(element, text_output)
        text_output.write("\n")
