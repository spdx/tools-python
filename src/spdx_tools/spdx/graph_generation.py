# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import Dict, List, Union

from spdx_tools.spdx.model import File, Package, Snippet

try:
    from networkx import DiGraph
except ImportError:
    DiGraph = None
from spdx_tools.spdx.document_utils import get_contained_spdx_elements
from spdx_tools.spdx.model import Document, Relationship


def export_graph_from_document(document: Document, file_name: str) -> None:
    from networkx.drawing import nx_agraph

    graph = generate_relationship_graph_from_spdx(document)
    _color_nodes(graph)
    attributes_graph = nx_agraph.to_agraph(graph)  # convert to a pygraphviz graph
    attributes_graph.draw(file_name, prog="dot")


def generate_relationship_graph_from_spdx(document: Document) -> DiGraph:
    from networkx import DiGraph

    graph = DiGraph()
    graph.add_node(document.creation_info.spdx_id, element=document.creation_info)

    contained_elements: Dict[str, Union[Package, File, Snippet]] = get_contained_spdx_elements(document)
    contained_element_nodes = [(spdx_id, {"element": element}) for spdx_id, element in contained_elements.items()]
    graph.add_nodes_from(contained_element_nodes)

    relationships_by_spdx_id: Dict[str, List[Relationship]] = dict()
    for relationship in document.relationships:
        relationships_by_spdx_id.setdefault(relationship.spdx_element_id, []).append(relationship)

    for spdx_id, relationships in relationships_by_spdx_id.items():
        if spdx_id not in graph.nodes():
            # this will add any external spdx_id to the graph where we have no further information about the element,
            # to indicate that this node represents an element we add the attribute "element"
            graph.add_node(spdx_id, element=None)
        for relationship in relationships:
            relationship_node_key = relationship.spdx_element_id + "_" + relationship.relationship_type.name
            graph.add_node(relationship_node_key, comment=relationship.comment)
            graph.add_edge(relationship.spdx_element_id, relationship_node_key)
            # if the related spdx element is SpdxNone or SpdxNoAssertion we need a type conversion
            related_spdx_element_id = str(relationship.related_spdx_element_id)

            if related_spdx_element_id not in graph.nodes():
                # this will add any external spdx_id to the graph where we have no further information about
                # the element, to indicate that this node represents an element we add the attribute "element"
                graph.add_node(
                    related_spdx_element_id,
                    element=None,
                )
            graph.add_edge(relationship_node_key, related_spdx_element_id)

    return graph


def _color_nodes(graph: DiGraph) -> None:
    for node in graph.nodes():
        if "_" in node:
            # nodes representing a RelationshipType are concatenated with the spdx_element_id,
            # to only see the RelationshipType when rendering the graph to a picture we add
            # a label to these nodes
            graph.add_node(node, color="lightgreen", label=node.split("_", 1)[-1])
        elif node == "SPDXRef-DOCUMENT":
            graph.add_node(node, color="indianred2")
        else:
            graph.add_node(node, color="lightskyblue")
