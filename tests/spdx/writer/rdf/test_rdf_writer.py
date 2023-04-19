# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import os

import pytest

from spdx_tools.spdx.model import Document
from spdx_tools.spdx.writer.rdf.rdf_writer import write_document_to_file
from tests.spdx.fixtures import document_fixture


@pytest.fixture
def temporary_file_path() -> str:
    temporary_file_path = "temp_test_rdf_writer_output.rdf.xml"
    yield temporary_file_path
    os.remove(temporary_file_path)


def test_write_document_to_file(temporary_file_path: str):
    document: Document = document_fixture()

    write_document_to_file(document, temporary_file_path, False)
