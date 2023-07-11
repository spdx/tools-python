# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import IO

from rdflib import Graph
from rdflib.compare import to_isomorphic

from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx3.rdfschema.namespace import (
    AI_NS,
    BUILD_NS,
    CORE_NS,
    DATASET_NS,
    LICENSING_NS,
    SECURITY_NS,
    SOFTWARE_NS,
)
from spdx_tools.spdx3.writer.rdf.converters.converter import model_to_rdf


def write_payload_to_stream(payload: Payload, stream: IO[bytes]):
    graph = Graph()
    for element in payload.get_full_map().values():
        model_to_rdf(element, graph)

    graph = to_isomorphic(graph)
    graph.bind("ai", AI_NS)
    graph.bind("build", BUILD_NS)
    graph.bind("core", CORE_NS)
    graph.bind("dataset", DATASET_NS)
    graph.bind("licensing", LICENSING_NS)
    graph.bind("security", SECURITY_NS)
    graph.bind("software", SOFTWARE_NS)
    graph.serialize(stream, "pretty-xml", encoding="UTF-8", max_depth=100)


def write_payload_to_file(payload: Payload, file_name: str):
    with open(file_name, "wb") as file:
        write_payload_to_stream(payload, file)
