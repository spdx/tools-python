# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import Dict
from rdflib import RDF, RDFS, BNode, Graph, Literal, URIRef

from spdx_tools.spdx.casing_tools import snake_case_to_camel_case
from spdx_tools.spdx.datetime_conversions import datetime_to_iso_string
from spdx_tools.spdx.model import Annotation
from spdx_tools.spdx.rdfschema.namespace import SPDX_NAMESPACE
from spdx_tools.spdx.writer.rdf.writer_utils import add_namespace_to_spdx_id


def add_annotation_to_graph(
    annotation: Annotation, graph: Graph, doc_namespace: str, external_doc_ref_to_namespace: Dict[str, str]
):
    annotation_resource = URIRef(
        add_namespace_to_spdx_id(annotation.spdx_id, doc_namespace, external_doc_ref_to_namespace)
    )
    annotation_node = BNode()
    graph.add((annotation_node, RDF.type, SPDX_NAMESPACE.Annotation))
    graph.add(
        (
            annotation_node,
            SPDX_NAMESPACE.annotationType,
            SPDX_NAMESPACE[f"annotationType_{snake_case_to_camel_case(annotation.annotation_type.name)}"],
        )
    )
    graph.add((annotation_node, SPDX_NAMESPACE.annotator, Literal(annotation.annotator.to_serialized_string())))
    graph.add(
        (annotation_node, SPDX_NAMESPACE.annotationDate, Literal(datetime_to_iso_string(annotation.annotation_date)))
    )
    graph.add((annotation_node, RDFS.comment, Literal(annotation.annotation_comment)))

    graph.add((annotation_resource, SPDX_NAMESPACE.annotation, annotation_node))
