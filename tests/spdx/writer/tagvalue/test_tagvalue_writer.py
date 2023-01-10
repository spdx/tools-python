#  Copyright (c) 2022 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os

import pytest

from tests.spdx.fixtures import document_fixture
from spdx.writer.tagvalue.tagvalue_writer import write_document_to_file


@pytest.fixture
def temporary_file_path() -> str:
    temporary_file_path = "temp_test_tag_value_writer_output.spdx"
    yield temporary_file_path
    os.remove(temporary_file_path)


def test_write_tag_value(temporary_file_path: str):
    document = document_fixture()

    write_document_to_file(document, temporary_file_path)

    # without a tag-value parser we can only test that no errors occur while writing
    # as soon as the tag-value parser is implemented (https://github.com/spdx/tools-python/issues/382) we can test for equality between the temporary file and the expected file in ./expected_results
