# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from rdflib import RDF, RDFS, Graph, Literal, URIRef

from spdx_tools.spdx.datetime_conversions import datetime_to_iso_string
from spdx_tools.spdx.rdfschema.namespace import LICENSE_NAMESPACE, SPDX_NAMESPACE
from spdx_tools.spdx.writer.rdf.creation_info_writer import add_creation_info_to_graph
from tests.spdx.fixtures import creation_info_fixture


def test_add_creation_info_to_graph():
    graph = Graph()
    creation_info = creation_info_fixture()

    add_creation_info_to_graph(creation_info, graph)

    assert (None, RDF.type, SPDX_NAMESPACE.SpdxDocument) in graph
    assert (URIRef(f"{creation_info.document_namespace}#{creation_info.spdx_id}"), None, None) in graph
    assert (None, SPDX_NAMESPACE.dataLicense, LICENSE_NAMESPACE[creation_info.data_license]) in graph
    assert (None, SPDX_NAMESPACE.name, Literal(creation_info.name)) in graph
    assert (None, SPDX_NAMESPACE.specVersion, Literal(creation_info.spdx_version)) in graph
    assert (None, SPDX_NAMESPACE.creationInfo, None) in graph

    assert (None, RDF.type, SPDX_NAMESPACE.CreationInfo) in graph
    assert (None, SPDX_NAMESPACE.created, Literal(datetime_to_iso_string(creation_info.created))) in graph
    assert (None, RDFS.comment, Literal(creation_info.creator_comment)) in graph
    assert (None, SPDX_NAMESPACE.licenseListVersion, Literal(creation_info.license_list_version)) in graph
    assert (None, SPDX_NAMESPACE.creator, Literal(creation_info.creators[0].to_serialized_string())) in graph
