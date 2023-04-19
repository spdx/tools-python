# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import os
from datetime import datetime

from rdflib import BNode, Graph, URIRef

from spdx_tools.spdx.model import Actor, ActorType, AnnotationType
from spdx_tools.spdx.parser.rdf.annotation_parser import parse_annotation
from spdx_tools.spdx.rdfschema.namespace import SPDX_NAMESPACE


def test_parse_annotation():
    graph = Graph().parse(os.path.join(os.path.dirname(__file__), "data/file_to_test_rdf_parser.rdf.xml"))
    doc_namespace = "https://some.namespace"
    file_node = URIRef(f"{doc_namespace}#SPDXRef-File")
    annotation_node = graph.value(subject=file_node, predicate=SPDX_NAMESPACE.annotation)
    assert isinstance(annotation_node, BNode)

    annotation = parse_annotation(annotation_node, graph, file_node, doc_namespace)

    assert annotation.spdx_id == "SPDXRef-File"
    assert annotation.annotation_type == AnnotationType.REVIEW
    assert annotation.annotator == Actor(ActorType.PERSON, "annotatorName", "some@mail.com")
    assert annotation.annotation_date == datetime(2022, 12, 1, 0, 0)
    assert annotation.annotation_comment == "annotationComment"
