# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import json
import os
# from rdflib import JsonLDParser
from rdflib import Graph, URIRef, Literal

from spdx_tools.spdx3.payload import Payload
# from spdx_tools.spdx3.writer.json_ld.json_ld_converter import convert_payload_to_json_ld_list_of_elements

def parse_from_file(file_name: str, encoding: str = "utf-8") -> Payload:
    return JsonLDParser().parseFile(file_name, encoding)

def parse_from_string(file_name: str) -> Payload:
    return JsonLDParser().parseString(file_name)


class JsonLDParser:
    # logger: Logger

    # def __init__(self):
    #     self.logger = Logger()

    def graphToPayload(self, graph: Graph) -> Payload:
        pass

    def parseString(self, data: str) -> Payload:
        graph = Graph().parse(data=data, format='json-ld')
        return self.graphToPayload(graph)

    def parseFile(self, file_name: str, encoding: str = "utf-8") -> Payload:
        with open(file_name, "r", encoding=encoding) as file:
            data = file.read()
            return self.parseStringToGraph(data)
