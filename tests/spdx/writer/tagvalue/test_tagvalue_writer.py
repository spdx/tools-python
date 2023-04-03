# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

import os

import pytest

from spdx.parser.tagvalue import tagvalue_parser
from spdx.writer.tagvalue.tagvalue_writer import write_document_to_file
from tests.spdx.fixtures import document_fixture


@pytest.fixture
def temporary_file_path() -> str:
    temporary_file_path = "temp_test_tag_value_writer_output.spdx"
    yield temporary_file_path
    os.remove(temporary_file_path)


def test_write_tag_value(temporary_file_path: str):
    document = document_fixture()

    write_document_to_file(document, temporary_file_path, False)

    parsed_document = tagvalue_parser.parse_from_file(temporary_file_path)

    assert parsed_document == document
