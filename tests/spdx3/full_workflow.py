# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import filecmp
import os

import pytest
from spdx.fixtures import document_fixture

from spdx_tools.spdx3.bump_from_spdx2.spdx_document import bump_spdx_document
from spdx_tools.spdx3.parser.json.json_parser import parse_from_file
from spdx_tools.spdx3.writer.json_ld.json_ld_writer import write_payload


@pytest.fixture
def temporary_file_paths() -> str:
    temporary_file_paths = ["temp_json_writer_output1.json", "temp_json_writer_output2.json"]
    yield temporary_file_paths
    os.remove(temporary_file_paths[0])
    os.remove(temporary_file_paths[1])


def test_full_workflow(temporary_file_paths):
    # this tests conversion->writing->parsing->writing and checks whether the same thing has been written twice
    spdx2_document = document_fixture()
    payload = bump_spdx_document(spdx2_document)

    write_payload(payload, temporary_file_paths[0])
    parsed_payload = parse_from_file(temporary_file_paths[0])

    write_payload(parsed_payload, temporary_file_paths[1])

    assert filecmp.cmp(temporary_file_paths[0], temporary_file_paths[1])
