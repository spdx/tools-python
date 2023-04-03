# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import os

import pytest

from spdx.model.document import Document
from spdx.parser.rdf import rdf_parser
from spdx.validation.document_validator import validate_full_spdx_document


def test_rdf_parser_file_not_found():
    with pytest.raises(FileNotFoundError, match="No such file or directory"):
        wrong_file_path = os.path.join(os.path.dirname(__file__), "hnjfkjsedhnflsiafg.json")
        rdf_parser.parse_from_file(wrong_file_path)


def test_rdf_parser_with_2_3_example():
    doc = rdf_parser.parse_from_file(
        os.path.join(os.path.dirname(__file__), "../../data/formats/SPDXRdfExample-v2.3.spdx.rdf.xml")
    )
    validation_messages = validate_full_spdx_document(doc)

    assert validation_messages == []
    assert type(doc) == Document
    assert len(doc.snippets) == 1
    assert len(doc.files) == 5
    assert len(doc.annotations) == 5
    assert len(doc.packages) == 4
    assert len(doc.relationships) == 13
    assert len(doc.extracted_licensing_info) == 5


def test_rdf_parser_with_2_2_example():
    doc = rdf_parser.parse_from_file(
        os.path.join(os.path.dirname(__file__), "../../data/formats/SPDXRdfExample-v2.2.spdx.rdf.xml")
    )
    validation_messages = validate_full_spdx_document(doc)

    assert validation_messages == []
    assert type(doc) == Document
    assert len(doc.snippets) == 1
    assert len(doc.files) == 4
    assert len(doc.annotations) == 5
    assert len(doc.packages) == 4
    assert len(doc.relationships) == 9
    assert len(doc.extracted_licensing_info) == 5
