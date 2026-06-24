# SPDX-FileCopyrightText: 2024 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import io
from datetime import datetime

from semantic_version import Version

from spdx_tools.spdx3.model import CreationInfo, SpdxDocument
from spdx_tools.spdx3.writer.console.spdx_document_writer import write_spdx_document


def test_render_creation_info():
    fake_datetime = datetime(year=2024, month=1, day=1)
    spec_version = Version("3.0.0")
    creation_info = CreationInfo(
        spec_version=spec_version,
        created=fake_datetime,
        created_by=[],
    )
    spdx_document = SpdxDocument(
        spdx_id="SPDXRef-FOO",
        name="BAR",
        element=[],
        root_element=[],
        creation_info=creation_info,
    )
    output_str = io.StringIO()
    write_spdx_document(spdx_document, text_output=output_str)

    assert output_str.getvalue() == """\
## SPDX Document
SPDXID: SPDXRef-FOO
name: BAR
# Creation Information
  specVersion: 3.0.0
  created: 2024-01-01T00:00:00Z
elements: 
root elements: 
profile conformance: 
"""  # noqa: W291 # elements: are printed with a space
