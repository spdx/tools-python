#  SPDX-FileCopyrightText: 2023 spdx contributors
#
#  SPDX-License-Identifier: Apache-2.0
from os import path

from spdx_tools.spdx.graph_generation import export_graph_from_document
from spdx_tools.spdx.model import Document
from spdx_tools.spdx.parser.parse_anything import parse_file

# This example demonstrates how to generate a relationship graph for an SPDX2 document

# Provide a path to the input file
input_path = path.join(path.dirname(__file__), "..", "tests", "spdx", "data", "SPDXJSONExample-v2.3.spdx.json")
# Parse the file
document: Document = parse_file(input_path)
# Generate the graph (note: you need to have installed the optional dependencies networkx and pygraphviz)
export_graph_from_document(document, "graph.png")
