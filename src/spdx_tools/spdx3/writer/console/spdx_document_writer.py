# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model import SpdxDocument
from spdx_tools.spdx3.writer.console.bundle_writer import write_bundle
from spdx_tools.spdx3.writer.console.namespace_map_writer import write_namespace_map
from spdx_tools.spdx.writer.tagvalue.tagvalue_writer_helper_functions import write_optional_heading


def write_spdx_document(spdx_document: SpdxDocument, text_output: TextIO):
    text_output.write("## SPDX Document\n")
    write_optional_heading(spdx_document.namespace_map, "# Namespace Map\n", text_output)
    for namespace_map in spdx_document.namespace_map:
        write_namespace_map(namespace_map, text_output)
    write_bundle(spdx_document, text_output, False)
