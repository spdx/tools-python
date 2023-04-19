# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from rdflib import RDF, RDFS, Graph, Literal, URIRef

from spdx_tools.spdx.datetime_conversions import datetime_to_iso_string
from spdx_tools.spdx.rdfschema.namespace import SPDX_NAMESPACE
from spdx_tools.spdx.writer.rdf.annotation_writer import add_annotation_to_graph
from tests.spdx.fixtures import annotation_fixture


def test_add_annotation_to_graph():
    graph = Graph()
    annotation = annotation_fixture()

    add_annotation_to_graph(annotation, graph, "docNamespace", {})

    assert (URIRef("docNamespace#SPDXRef-File"), SPDX_NAMESPACE.annotation, None) in graph
    assert (None, RDF.type, SPDX_NAMESPACE.Annotation) in graph
    assert (None, SPDX_NAMESPACE.annotationType, SPDX_NAMESPACE.annotationType_review) in graph
    assert (None, SPDX_NAMESPACE.annotationDate, Literal(datetime_to_iso_string(annotation.annotation_date))) in graph
    assert (None, SPDX_NAMESPACE.annotator, Literal(annotation.annotator.to_serialized_string())) in graph
    assert (None, RDFS.comment, Literal(annotation.annotation_comment)) in graph
