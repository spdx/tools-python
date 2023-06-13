# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import os

from spdx_tools.spdx3.parser.json.json_parser import parse_from_file


def test_converted_document_parsing():
    parse_from_file(os.path.join(os.path.dirname(__file__), "../../data/json/spdx23_conversion.json"))


def test_single_package_parsing():
    parse_from_file(os.path.join(os.path.dirname(__file__), "../../data/json/single_package_example.json"))
