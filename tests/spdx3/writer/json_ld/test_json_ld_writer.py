# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from importlib import resources

from spdx_tools.spdx3.bump_from_spdx2.spdx_document import bump_spdx_document
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx3.writer.json_ld.json_ld_writer import write_payload
from spdx_tools.spdx.model.document import Document as Spdx2_Document
from tests.spdx.fixtures import document_fixture


def test_json_writer():
    spdx2_document: Spdx2_Document = document_fixture()
    payload: Payload = bump_spdx_document(spdx2_document)

    # this currently generates an actual file to look at, this should be changed to a temp file later
    with resources.as_file(resources.files("tests.spdx3.writer.json_ld").joinpath("SPDX3_jsonld_test")) as output_file:
        write_payload(payload, str(output_file))
