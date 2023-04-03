# SPDX-FileCopyrightText: 2023 spdx contributors

# SPDX-License-Identifier: Apache-2.0
from typing import TextIO

from spdx3.model.annotation import Annotation
from spdx3.model.bom import Bom
from spdx3.model.bundle import Bundle
from spdx3.model.organization import Organization
from spdx3.model.person import Person
from spdx3.model.relationship import Relationship
from spdx3.model.software.file import File
from spdx3.model.software.package import Package
from spdx3.model.software.sbom import Sbom
from spdx3.model.software.snippet import Snippet
from spdx3.model.software_agent import SoftwareAgent
from spdx3.model.spdx_document import SpdxDocument
from spdx3.model.tool import Tool
from spdx3.payload import Payload
from spdx3.writer.console.agent_writer import write_agent
from spdx3.writer.console.annotation_writer import write_annotation
from spdx3.writer.console.bom_writer import write_bom
from spdx3.writer.console.bundle_writer import write_bundle
from spdx3.writer.console.relationship_writer import write_relationship
from spdx3.writer.console.software.file_writer import write_file
from spdx3.writer.console.software.package_writer import write_package
from spdx3.writer.console.software.sbom_writer import write_sbom
from spdx3.writer.console.software.snippet_writer import write_snippet
from spdx3.writer.console.spdx_document_writer import write_spdx_document
from spdx3.writer.console.tool_writer import write_tool

MAP_CLASS_TO_WRITE_METHOD = {
    Annotation: write_annotation,
    Relationship: write_relationship,
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
}


def write_payload(payload: Payload, text_output: TextIO):
    for element in payload.get_full_map().values():
        write_method = MAP_CLASS_TO_WRITE_METHOD[type(element)]
        write_method(element, text_output)
        text_output.write("\n")
