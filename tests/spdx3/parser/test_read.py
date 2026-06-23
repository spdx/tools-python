# SPDX-FileCopyrightText: 2026-present SPDX contributors
# SPDX-License-Identifier: Apache-2.0
import os

import pytest

from spdx_tools.spdx3.object_set import SpdxObjectSet
from spdx_tools.spdx3.parser import parse_file
from spdx_tools.spdx.parser.error import SPDXParsingError

EXAMPLE_FILE = os.path.join(os.path.dirname(__file__), os.pardir, "data", "example.spdx3.json")


def test_parse_file_returns_object_set():
    object_set = parse_file(EXAMPLE_FILE)

    assert isinstance(object_set, SpdxObjectSet)

    elements = list(object_set.foreach())
    assert len(elements) == 60

    relationships = list(object_set.foreach_type("Relationship"))
    assert len(relationships) == 28


def test_parse_file_find_by_id():
    object_set = parse_file(EXAMPLE_FILE)

    spdx_id = "http://spdx.org/spdxdocs/examplemaven-0.0.1/enriched-specv3/SPDXRef-gnrtd0"
    element = object_set.find_by_id(spdx_id)

    assert element is not None
    assert str(element._id) == spdx_id


def test_parse_file_unsupported_extension():
    with pytest.raises(SPDXParsingError):
        parse_file("some_file.rdf")
