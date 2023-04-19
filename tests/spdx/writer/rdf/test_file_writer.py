# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from rdflib import RDF, RDFS, Graph, Literal, URIRef

from spdx_tools.spdx.rdfschema.namespace import LICENSE_NAMESPACE, SPDX_NAMESPACE
from spdx_tools.spdx.writer.rdf.file_writer import add_file_to_graph
from tests.spdx.fixtures import file_fixture


def test_add_file_to_graph():
    graph = Graph()
    file = file_fixture()

    add_file_to_graph(file, graph, "docNamespace", {})

    assert (URIRef("docNamespace#SPDXRef-File"), RDF.type, SPDX_NAMESPACE.File) in graph
    assert (None, SPDX_NAMESPACE.fileName, Literal(file.name)) in graph
    assert (None, SPDX_NAMESPACE.fileType, SPDX_NAMESPACE.fileType_text) in graph
    assert (None, SPDX_NAMESPACE.licenseComments, Literal(file.license_comment)) in graph
    assert (None, SPDX_NAMESPACE.licenseConcluded, None) in graph
    assert (None, SPDX_NAMESPACE.licenseInfoInFile, LICENSE_NAMESPACE.MIT) in graph
    assert (None, SPDX_NAMESPACE.licenseInfoInFile, LICENSE_NAMESPACE["GPL-2.0-only"]) in graph
    assert (None, SPDX_NAMESPACE.licenseInfoInFile, SPDX_NAMESPACE.noassertion) in graph
    assert (None, SPDX_NAMESPACE.copyrightText, Literal(file.copyright_text)) in graph
    assert (None, RDFS.comment, Literal(file.comment)) in graph
    assert (None, SPDX_NAMESPACE.noticeText, Literal(file.notice)) in graph
    assert (None, SPDX_NAMESPACE.fileContributor, Literal(file.contributors[0])) in graph
    assert (None, SPDX_NAMESPACE.checksum, None) in graph
    assert (None, SPDX_NAMESPACE.attributionText, Literal(file.attribution_texts[0])) in graph
