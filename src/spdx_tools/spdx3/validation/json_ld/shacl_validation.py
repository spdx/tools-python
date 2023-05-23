# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import Optional

import owlrl
from pyshacl import validate
from rdflib import Graph, RDF


def validate_against_shacl_from_file(
    data_file: str, shacl_file: str, data_format: Optional[str] = "json-ld", shacl_format: Optional[str] = "ttl"
):
    data_graph = Graph()
    with open(data_file) as file:
        data_graph.parse(file, format=data_format)

    shacl_graph = Graph()
    with open(shacl_file) as file:
        shacl_graph.parse(file, format=shacl_format)

    # we need to copy the named individuals created for our vocabulary types to
    # an extra ontology graph since pySHACL ignores them in the provided shacl graph.
    # if not provided in the ontology graph, validation fails due to those objects not being defined.
    ont_graph = Graph()
    named_individuals = shacl_graph.subjects(RDF.type, owlrl.OWL.NamedIndividual)
    for named_individual in named_individuals:
        ont_graph += shacl_graph.triples((named_individual, None, None))

    return validate(data_graph=data_graph, shacl_graph=shacl_graph, ont_graph=ont_graph)
