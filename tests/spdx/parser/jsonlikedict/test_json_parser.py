import os

from spdx_tools.spdx.parser.json import json_parser


def test_parse_control_characters():
    doc = json_parser.parse_from_file(
        os.path.join(os.path.dirname(__file__), "../../data/ControlCharacters.spdx.json")
    )
    assert doc.creation_info.creators[0].name == "Nisha  K"
    assert doc.extracted_licensing_info[0].extracted_text == 'Golang BSD plus Patents "\\/\n\r\t'
