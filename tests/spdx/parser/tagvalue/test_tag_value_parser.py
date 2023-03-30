# Copyright (c) 2014 Ahmed H. Ismail
# SPDX-FileCopyrightText: 2023 spdx contributors

# SPDX-License-Identifier: Apache-2.0
import os

import pytest

from spdx.model.document import Document
from spdx.model.relationship import Relationship, RelationshipType
from spdx.parser.error import SPDXParsingError
from spdx.parser.tagvalue.parser import Parser
from tests.spdx.parser.tagvalue.test_creation_info_parser import DOCUMENT_STR


def test_parse_unknown_tag():
    parser = Parser()
    unknown_tag_str = "UnknownTag: This is an example for an unknown tag."

    with pytest.raises(SPDXParsingError, match="Unknown tag"):
        parser.parse(unknown_tag_str)


def test_tag_value_parser():
    parser = Parser()
    fn = os.path.join(os.path.dirname(__file__), "../../data/formats/SPDXTagExample-v2.3.spdx")

    with open(fn) as f:
        data = f.read()
        doc = parser.parse(data)
    assert type(doc) == Document
    assert len(doc.annotations) == 5
    assert len(doc.files) == 5
    assert len(doc.packages) == 4
    assert len(doc.snippets) == 1
    assert len(doc.relationships) == 13
    assert len(doc.extracted_licensing_info) == 5


def test_building_contains_relationship():
    parser = Parser()
    document_str = "\n".join(
        [
            DOCUMENT_STR,
            "FileName: File without package",
            "SPDXID: SPDXRef-File",
            "FileChecksum: SHA1: d6a770ba38583ed4bb4525bd96e50461655d2759",
            "PackageName: Package with two files",
            "SPDXID: SPDXRef-Package-with-two-files",
            "PackageDownloadLocation: https://download.com",
            "FileName: File in package",
            "SPDXID: SPDXRef-File-in-Package",
            "FileChecksum: SHA1: d6a770ba38583ed4bb4525bd96e50461655d2759",
            "FileName: Second file in package",
            "SPDXID: SPDXRef-Second-File-in-Package",
            "FileChecksum: SHA1: d6a770ba38583ed4bb4525bd96e50461655d2759",
            "PackageName: Second package with file",
            "SPDXID: SPDXRef-Package-with-one-file",
            "PackageDownloadLocation: https://download.com",
            "FileName: File in package",
            "SPDXID: SPDXRef-File-in-different-Package",
            "FileChecksum: SHA1: d6a770ba38583ed4bb4525bd96e50461655d2759",
        ]
    )
    document = parser.parse(document_str)

    assert document.relationships == [
        Relationship("SPDXRef-Package-with-two-files", RelationshipType.CONTAINS, "SPDXRef-File-in-Package"),
        Relationship("SPDXRef-Package-with-two-files", RelationshipType.CONTAINS, "SPDXRef-Second-File-in-Package"),
        Relationship("SPDXRef-Package-with-one-file", RelationshipType.CONTAINS, "SPDXRef-File-in-different-Package"),
    ]


def test_document_with_mixed_values():
    parser = Parser()
    document_str = "\n".join(
        [
            "SPDXID:SPDXRef-DOCUMENT",
            "FileName: File without package",
            "SPDXID: SPDXRef-File",
            "PackageDownloadLocation: https://download.com",
            "FileChecksum: SHA1: d6a770ba38583ed4bb4525bd96e50461655d2759",
        ]
    )

    with pytest.raises(SPDXParsingError) as err:
        parser.parse(document_str)

    assert err.value.get_messages() == [
        "Element Package is not the current element in scope, probably the expected "
        "tag to start the element (PackageName) is missing. Line: 4"
    ]
