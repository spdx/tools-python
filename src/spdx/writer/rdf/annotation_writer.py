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
from typing import Dict

from rdflib import Graph, Literal, RDFS, URIRef, RDF, BNode

from spdx.datetime_conversions import datetime_to_iso_string
from spdx.model.annotation import Annotation
from spdx.casing_tools import snake_case_to_camel_case
from spdx.writer.rdf.writer_utils import add_namespace_to_spdx_id
from spdx.rdfschema.namespace import SPDX_NAMESPACE


def add_annotation_to_graph(annotation: Annotation, graph: Graph, doc_namespace: str,
                            external_doc_ref_to_namespace: Dict[str, str]):
    annotation_resource = URIRef(add_namespace_to_spdx_id(annotation.spdx_id, doc_namespace, external_doc_ref_to_namespace))
    annotation_node = BNode()
    graph.add((annotation_node, RDF.type, SPDX_NAMESPACE.Annotation))
    graph.add((annotation_node, SPDX_NAMESPACE.annotationType,
               SPDX_NAMESPACE[f"annotationType_{snake_case_to_camel_case(annotation.annotation_type.name)}"]))
    graph.add((annotation_node, SPDX_NAMESPACE.annotator, Literal(annotation.annotator.to_serialized_string())))
    graph.add(
        (annotation_node, SPDX_NAMESPACE.annotationDate, Literal(datetime_to_iso_string(annotation.annotation_date))))
    graph.add((annotation_node, RDFS.comment, Literal(annotation.annotation_comment)))

    graph.add((annotation_resource, SPDX_NAMESPACE.annotation, annotation_node))
