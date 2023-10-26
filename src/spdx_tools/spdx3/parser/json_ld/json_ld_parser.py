# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import json
import os
# from rdflib import JsonLDParser
from rdflib import Graph, URIRef, Literal

from spdx_tools.spdx3.payload import Payload
# from spdx_tools.spdx3.writer.json_ld.json_ld_converter import convert_payload_to_json_ld_list_of_elements

class JsonLDParser:
    logger: Logger

    def __init__(self):
        self.logger = Logger()

    def parseFileToGraph(self, file_name: str) -> Graph:
        with open(file_name, "r") as file:
            # read file to string
            data = file.read()
            return Graph().parse(data=data, format='json-ld')

    def graphToPayload(self, graph: Graph) -> Payload:
        pass

    def parseToPayload(self, file_name: str) -> Payload:
        graph = self.parseFileToGraph(file_name)
        return self.graphToPayload(graph)
