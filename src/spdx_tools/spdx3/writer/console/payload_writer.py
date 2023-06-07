# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model import (
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
from spdx_tools.spdx3.model.ai import AIPackage
from spdx_tools.spdx3.model.build import Build
from spdx_tools.spdx3.model.dataset import Dataset
from spdx_tools.spdx3.model.software import File, Package, Sbom, Snippet, SoftwareDependencyRelationship
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx3.writer.console.agent_writer import write_agent
from spdx_tools.spdx3.writer.console.ai.ai_package_writer import write_ai_package
from spdx_tools.spdx3.writer.console.annotation_writer import write_annotation
from spdx_tools.spdx3.writer.console.bom_writer import write_bom
from spdx_tools.spdx3.writer.console.build.build_writer import write_build
from spdx_tools.spdx3.writer.console.bundle_writer import write_bundle
from spdx_tools.spdx3.writer.console.dataset.dataset_writer import write_dataset
from spdx_tools.spdx3.writer.console.relationship_writer import write_relationship
from spdx_tools.spdx3.writer.console.software.file_writer import write_file
from spdx_tools.spdx3.writer.console.software.package_writer import write_package
from spdx_tools.spdx3.writer.console.software.sbom_writer import write_sbom
from spdx_tools.spdx3.writer.console.software.snippet_writer import write_snippet
from spdx_tools.spdx3.writer.console.software.software_dependency_relationship_writer import (
    write_software_dependency_relationship,
)
from spdx_tools.spdx3.writer.console.spdx_document_writer import write_spdx_document
from spdx_tools.spdx3.writer.console.tool_writer import write_tool

MAP_CLASS_TO_WRITE_METHOD = {
    Annotation: write_annotation,
    Relationship: write_relationship,
    SoftwareDependencyRelationship: write_software_dependency_relationship,
    Bundle: write_bundle,
    SpdxDocument: write_spdx_document,
    Bom: write_bom,
    File: write_file,
    Package: write_package,
    Snippet: write_snippet,
    Sbom: write_sbom,
    Person: write_agent,
    Organization: write_agent,
    SoftwareAgent: write_agent,
    Tool: write_tool,
    AIPackage: write_ai_package,
    Dataset: write_dataset,
    Build: write_build,
}


def write_payload(payload: Payload, text_output: TextIO):
    for element in payload.get_full_map().values():
        write_method = MAP_CLASS_TO_WRITE_METHOD[type(element)]
        write_method(element, text_output)
        text_output.write("\n")
