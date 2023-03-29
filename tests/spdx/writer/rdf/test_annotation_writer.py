# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from rdflib import Graph, Literal, RDFS, URIRef, RDF

from spdx.datetime_conversions import datetime_to_iso_string
from spdx.writer.rdf.annotation_writer import add_annotation_to_graph
from spdx.rdfschema.namespace import SPDX_NAMESPACE
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
