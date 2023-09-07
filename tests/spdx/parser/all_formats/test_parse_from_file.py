# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

import os

import pytest

from spdx_tools.spdx.model import Document
from spdx_tools.spdx.parser.json import json_parser
from spdx_tools.spdx.parser.rdf import rdf_parser
from spdx_tools.spdx.parser.tagvalue import tagvalue_parser
from spdx_tools.spdx.parser.xml import xml_parser
from spdx_tools.spdx.parser.yaml import yaml_parser


@pytest.mark.parametrize(
    "parser, format_name, extension",
    [
        (json_parser, "JSON", ".json"),
        (xml_parser, "XML", ".xml"),
        (yaml_parser, "YAML", ".yaml"),
        (rdf_parser, "Rdf", ".rdf.xml"),
        (tagvalue_parser, "Tag", ""),
    ],
)
class TestParseFromFile:
    def test_parse_from_file_not_found(self, parser, format_name, extension):
        with pytest.raises(FileNotFoundError) as err:
            wrong_file_path = os.path.join(os.path.dirname(__file__), f"hnjfkjsedhnflsiafg.spdx{extension}")
            parser.parse_from_file(wrong_file_path)

        assert err.value.args[1] == "No such file or directory"

    def test_parse_from_file_with_2_3_example(self, parser, format_name, extension):
        doc = parser.parse_from_file(
            os.path.join(os.path.dirname(__file__), f"../../data/SPDX{format_name}Example-v2.3.spdx{extension}")
        )
        assert isinstance(doc, Document)
        assert len(doc.annotations) == 5
        assert len(doc.files) == 5
        assert len(doc.packages) == 4
        assert len(doc.snippets) == 1
        assert len(doc.relationships) == 13
        assert len(doc.extracted_licensing_info) == 5

    def test_parse_from_file_with_2_2_example(self, parser, format_name, extension):
        doc = parser.parse_from_file(
            os.path.join(os.path.dirname(__file__), f"../../data/SPDX{format_name}Example-v2.2.spdx{extension}")
        )
        assert isinstance(doc, Document)
        assert len(doc.annotations) == 5
        assert len(doc.files) == 4
        assert len(doc.packages) == 4
        assert len(doc.snippets) == 1
        assert len(doc.relationships) == 11
        assert len(doc.extracted_licensing_info) == 5

    def test_parse_from_file_with_encoding_example(self, parser, format_name, extension):
        doc = parser.parse_from_file(
            os.path.join(os.path.dirname(__file__), f"../../data/SPDX{format_name}Example-UTF-16.spdx{extension}"),
            "utf-16",
        )
        assert isinstance(doc, Document)
        assert len(doc.annotations) == 5
        assert len(doc.files) == 4
        assert len(doc.packages) == 4
        assert len(doc.snippets) == 1
        assert len(doc.relationships) == 11
        assert len(doc.extracted_licensing_info) == 5
