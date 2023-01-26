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
from datetime import datetime

from rdflib import Graph, Literal, RDFS

from spdx.datetime_conversions import datetime_to_iso_string
from spdx.writer.rdf.annotation_writer import add_annotation_info_to_graph
from spdx.writer.rdf.writer_utils import spdx_namespace
from tests.spdx.fixtures import annotation_fixture


def test_add_annotation_info_to_graph():
    graph = Graph()
    annotation = annotation_fixture()

    add_annotation_info_to_graph(annotation, graph, "anyURI", {})

    assert (None, None, spdx_namespace.Annotation) in graph
    assert (None, spdx_namespace.annotationType, spdx_namespace.annotationType_review) in graph
    assert (None, spdx_namespace.annotationDate, Literal(datetime_to_iso_string(datetime(2022, 12, 1)))) in graph
    assert (None, spdx_namespace.annotator, Literal("Person: annotatorName (some@mail.com)")) in graph
    assert (None, RDFS.comment, Literal("annotationComment")) in graph
