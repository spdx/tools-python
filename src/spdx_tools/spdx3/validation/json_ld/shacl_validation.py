# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import Optional
from pyshacl import validate
from rdflib import Graph


def validate_against_shacl_from_file(
    data_file: str, shacl_file: str, data_format: Optional[str] = "json-ld", shacl_format: Optional[str] = "ttl"
):
    data_graph = Graph()
    with open(data_file) as file:
        data_graph.parse(file, format=data_format)

    shacl_graph = Graph()
    with open(shacl_file) as file:
        shacl_graph.parse(file, format=shacl_format)

    return validate(data_graph=data_graph, shacl_graph=shacl_graph, ont_graph=shacl_graph)
