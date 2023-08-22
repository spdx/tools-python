# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import os
from unittest import TestCase

import pytest
from rdflib import RDF, BNode, Graph, URIRef

from spdx_tools.common.spdx_licensing import spdx_licensing
from spdx_tools.spdx.model import Checksum, ChecksumAlgorithm, FileType, SpdxNoAssertion
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.rdf.file_parser import parse_file
from spdx_tools.spdx.rdfschema.namespace import SPDX_NAMESPACE


def test_parse_file():
    graph = Graph().parse(os.path.join(os.path.dirname(__file__), "data/file_to_test_rdf_parser.rdf.xml"))
    file_node = graph.value(predicate=RDF.type, object=SPDX_NAMESPACE.File)
    doc_namespace = "https://some.namespace"
    assert isinstance(file_node, URIRef)

    file = parse_file(file_node, graph, doc_namespace)

    assert file.name == "./fileName.py"
    assert file.spdx_id == "SPDXRef-File"
    assert file.checksums == [Checksum(ChecksumAlgorithm.SHA1, "71c4025dd9897b364f3ebbb42c484ff43d00791c")]
    assert file.file_types == [FileType.TEXT]
    assert file.comment == "fileComment"
    assert file.copyright_text == "copyrightText"
    assert file.contributors == ["fileContributor"]
    assert file.license_concluded == spdx_licensing.parse("MIT AND GPL-2.0")
    TestCase().assertCountEqual(
        file.license_info_in_file,
        [spdx_licensing.parse("MIT"), spdx_licensing.parse("GPL-2.0"), SpdxNoAssertion()],
    )
    assert file.license_comment == "licenseComment"
    assert file.notice == "fileNotice"
    assert file.attribution_texts == ["fileAttributionText"]


def test_parse_invalid_file():
    graph = Graph().parse(os.path.join(os.path.dirname(__file__), "data/invalid_documents/file_without_spdx_ids.xml"))
    file_node = graph.value(predicate=RDF.type, object=SPDX_NAMESPACE.File)
    doc_namespace = "https://some.namespace"

    assert isinstance(file_node, BNode)
    with pytest.raises(SPDXParsingError):
        parse_file(file_node, graph, doc_namespace)
