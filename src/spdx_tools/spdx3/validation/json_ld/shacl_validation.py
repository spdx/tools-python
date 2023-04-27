# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from pyshacl import validate
from rdflib import Graph


def validate_against_shacl_from_file(data_file: str, shacl_file: str):
    data_graph = Graph()
    with open(data_file) as file:
        data_graph.parse(file, format="json-ld")

    shacl_graph = Graph()
    with open(shacl_file) as file:
        shacl_graph.parse(file, format="ttl")

    return validate_against_shacl(data_graph, shacl_graph)


def validate_against_shacl(data_graph: Graph, shacl_graph: Graph):
    return validate(data_graph=data_graph, shacl_graph=shacl_graph)
