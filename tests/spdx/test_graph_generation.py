# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from pathlib import Path
from typing import List
from unittest import TestCase

import pytest

from spdx_tools.spdx.graph_generation import generate_relationship_graph_from_spdx
from spdx_tools.spdx.model import Document, Relationship, RelationshipType
from spdx_tools.spdx.parser.parse_anything import parse_file
from tests.spdx.fixtures import document_fixture, file_fixture, package_fixture

try:
    import networkx  # noqa: F401
except ImportError:
    pytest.skip("Skip this module as the tests need optional dependencies to run.", allow_module_level=True)


@pytest.mark.parametrize(
    "file_name, nodes_count, edges_count, relationship_node_keys",
    [
        (
            "SPDXJSONExample-v2.3.spdx.json",
            22,
            22,
            ["SPDXRef-Package_DYNAMIC_LINK", "SPDXRef-JenaLib_CONTAINS"],
        ),
        (
            "SPDXJSONExample-v2.2.spdx.json",
            20,
            19,
            ["SPDXRef-Package_DYNAMIC_LINK", "SPDXRef-JenaLib_CONTAINS"],
        ),
        (
            "SPDXRdfExample-v2.3.spdx.rdf.xml",
            22,
            22,
            ["SPDXRef-Package_DYNAMIC_LINK", "SPDXRef-JenaLib_CONTAINS"],
        ),
        (
            "SPDXRdfExample-v2.2.spdx.rdf.xml",
            20,
            19,
            ["SPDXRef-Package_DYNAMIC_LINK", "SPDXRef-JenaLib_CONTAINS"],
        ),
        (
            "SPDXTagExample-v2.3.spdx",
            22,
            22,
            ["SPDXRef-Package_DYNAMIC_LINK", "SPDXRef-JenaLib_CONTAINS"],
        ),
    ],
)
def test_generate_graph_from_spdx(
    file_name: str,
    nodes_count: int,
    edges_count: int,
    relationship_node_keys: List[str],
) -> None:
    document = parse_file(str(Path(__file__).resolve().parent.parent / "spdx" / "data" / file_name))
    graph = generate_relationship_graph_from_spdx(document)

    assert document.creation_info.spdx_id in graph.nodes()
    assert graph.number_of_nodes() == nodes_count
    assert graph.number_of_edges() == edges_count
    assert "SPDXRef-DOCUMENT_DESCRIBES" in graph.nodes()
    for relationship_node_key in relationship_node_keys:
        assert relationship_node_key in graph.nodes()


def test_complete_connected_graph() -> None:
    document = _create_minimal_document()

    graph = generate_relationship_graph_from_spdx(document)

    TestCase().assertCountEqual(
        graph.nodes(),
        [
            "SPDXRef-DOCUMENT",
            "SPDXRef-Package-A",
            "SPDXRef-Package-B",
            "SPDXRef-File",
            "SPDXRef-DOCUMENT_DESCRIBES",
            "SPDXRef-Package-A_CONTAINS",
            "SPDXRef-Package-B_CONTAINS",
        ],
    )
    TestCase().assertCountEqual(
        graph.edges(),
        [
            ("SPDXRef-DOCUMENT", "SPDXRef-DOCUMENT_DESCRIBES"),
            ("SPDXRef-DOCUMENT_DESCRIBES", "SPDXRef-Package-A"),
            ("SPDXRef-DOCUMENT_DESCRIBES", "SPDXRef-Package-B"),
            ("SPDXRef-Package-A", "SPDXRef-Package-A_CONTAINS"),
            ("SPDXRef-Package-A_CONTAINS", "SPDXRef-File"),
            ("SPDXRef-Package-B", "SPDXRef-Package-B_CONTAINS"),
            ("SPDXRef-Package-B_CONTAINS", "SPDXRef-File"),
        ],
    )


def test_complete_unconnected_graph() -> None:
    document = _create_minimal_document()
    document.packages += [package_fixture(spdx_id="SPDXRef-Package-C", name="Package without connection to document")]

    graph = generate_relationship_graph_from_spdx(document)

    TestCase().assertCountEqual(
        graph.nodes(),
        [
            "SPDXRef-DOCUMENT",
            "SPDXRef-Package-A",
            "SPDXRef-Package-B",
            "SPDXRef-File",
            "SPDXRef-DOCUMENT_DESCRIBES",
            "SPDXRef-Package-A_CONTAINS",
            "SPDXRef-Package-B_CONTAINS",
            "SPDXRef-Package-C",
        ],
    )
    TestCase().assertCountEqual(
        graph.edges(),
        [
            ("SPDXRef-DOCUMENT", "SPDXRef-DOCUMENT_DESCRIBES"),
            ("SPDXRef-DOCUMENT_DESCRIBES", "SPDXRef-Package-A"),
            ("SPDXRef-DOCUMENT_DESCRIBES", "SPDXRef-Package-B"),
            ("SPDXRef-Package-A", "SPDXRef-Package-A_CONTAINS"),
            ("SPDXRef-Package-A_CONTAINS", "SPDXRef-File"),
            ("SPDXRef-Package-B", "SPDXRef-Package-B_CONTAINS"),
            ("SPDXRef-Package-B_CONTAINS", "SPDXRef-File"),
        ],
    )


def _create_minimal_document() -> Document:
    packages = [
        package_fixture(spdx_id="SPDXRef-Package-A", name="Package-A"),
        package_fixture(spdx_id="SPDXRef-Package-B", name="Package-B"),
    ]
    files = [
        file_fixture(spdx_id="SPDXRef-File", name="File"),
    ]
    relationships = [
        Relationship("SPDXRef-DOCUMENT", RelationshipType.DESCRIBES, "SPDXRef-Package-A"),
        Relationship("SPDXRef-DOCUMENT", RelationshipType.DESCRIBES, "SPDXRef-Package-B"),
        Relationship("SPDXRef-Package-A", RelationshipType.CONTAINS, "SPDXRef-File"),
        Relationship("SPDXRef-Package-B", RelationshipType.CONTAINS, "SPDXRef-File"),
    ]
    document = document_fixture(packages=packages, files=files, relationships=relationships, snippets=[])

    return document
