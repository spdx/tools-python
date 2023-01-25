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
from rdflib import Graph, Literal, RDFS, URIRef, RDF, BNode

from spdx.datetime_conversions import datetime_to_iso_string
from spdx.model.annotation import Annotation
from spdx.writer.casing_tools import snake_case_to_camel_case
from spdx.writer.rdf.writer_utils import spdx_namespace


def add_annotation_info_to_graph(annotation: Annotation, graph: Graph, doc_namespace: str):
    annotation_resource = URIRef(f"{doc_namespace}#{annotation.spdx_id}")
    annotation_node = BNode()
    graph.add((annotation_node, RDF.type, spdx_namespace.Annotation))
    graph.add((annotation_node, spdx_namespace.annotationType,
               spdx_namespace[f"annotationType_{snake_case_to_camel_case(annotation.annotation_type.name)}"]))
    graph.add((annotation_node, spdx_namespace.annotator, Literal(annotation.annotator.to_serialized_string())))
    graph.add(
        (annotation_node, spdx_namespace.annotationDate, Literal(datetime_to_iso_string(annotation.annotation_date))))
    graph.add((annotation_node, RDFS.comment, Literal(annotation.annotation_comment)))

    graph.add((annotation_resource, spdx_namespace.annotation, annotation_node))
