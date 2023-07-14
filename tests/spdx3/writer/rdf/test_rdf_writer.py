# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import os

from spdx_tools.spdx3.bump_from_spdx2.spdx_document import bump_spdx_document
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx3.validation.rdf.shacl_validation import validate_against_shacl_from_file
from spdx_tools.spdx3.writer.rdf.rdf_writer import write_payload_to_file
from spdx_tools.spdx.model.document import Document as Spdx2_Document
from tests.spdx.fixtures import document_fixture


def test_rdf_writer():
    spdx2_document: Spdx2_Document = document_fixture()
    payload: Payload = bump_spdx_document(spdx2_document)

    # this currently generates an actual file to look at, this should be changed to a temp file later
    write_payload_to_file(payload, os.path.join(os.path.dirname(__file__), "test.rdf"))

    conforms, _, results_text = validate_against_shacl_from_file(
        data_file=os.path.join(os.path.dirname(__file__), "test.rdf"),
        shacl_file=os.path.join(
            os.path.dirname(__file__), "../../../../src/spdx_tools/spdx3/validation/rdf/model.ttl"
        ),
        data_format="xml",
    )
    print(results_text)
    # TODO: enable this assertion once all shacl validation issues have been fixed
    # assert conforms
