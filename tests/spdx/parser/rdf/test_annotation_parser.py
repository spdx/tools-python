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
import os
from datetime import datetime

from rdflib import Graph, URIRef

from spdx.model.actor import Actor, ActorType
from spdx.model.annotation import AnnotationType
from spdx.parser.rdf.annotation_parser import parse_annotation
from spdx.rdfschema.namespace import SPDX_NAMESPACE


def test_parse_annotation():
    graph = Graph().parse(os.path.join(os.path.dirname(__file__), "data/file_to_test_rdf_parser.rdf.xml"))
    doc_namespace = "https://some.namespace"
    file_node = URIRef(f"{doc_namespace}#SPDXRef-File")
    annotation_node = graph.value(subject=file_node, predicate=SPDX_NAMESPACE.annotation)

    annotation = parse_annotation(annotation_node, graph, file_node, doc_namespace)

    assert annotation.spdx_id == "SPDXRef-File"
    assert annotation.annotation_type == AnnotationType.REVIEW
    assert annotation.annotator == Actor(ActorType.PERSON, "annotatorName", "some@mail.com")
    assert annotation.annotation_date == datetime(2022, 12, 1, 0, 0)
    assert annotation.annotation_comment == "annotationComment"
