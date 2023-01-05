# Copyright (c) 2022 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List

import pytest

from src.validation.snippet_validator import validate_snippet_within_document
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.fixtures import document_fixture, snippet_fixture


def test_valid_snippet():
    snippet = snippet_fixture()
    validation_messages: List[ValidationMessage] = validate_snippet_within_document(snippet, document_fixture())

    assert validation_messages == []


@pytest.mark.parametrize("snippet_input, expected_message",
                         [(snippet_fixture(byte_range=(-12, 45)),
                           "byte_range values must be greater than or equal to 1, but is: (-12, 45)"),
                          (snippet_fixture(byte_range=(45, 23)),
                           "the first value of byte_range must be less than or equal to the second, but is: (45, 23)"),
                          (snippet_fixture(line_range=(-12, 45)),
                           "line_range values must be greater than or equal to 1, but is: (-12, 45)"),
                          (snippet_fixture(line_range=(45, 23)),
                           "the first value of line_range must be less than or equal to the second, but is: (45, 23)")
                          ])
def test_invalid_ranges(snippet_input, expected_message):
    validation_messages: List[ValidationMessage] = validate_snippet_within_document(snippet_input, document_fixture())

    expected = ValidationMessage(expected_message,
                                 ValidationContext(spdx_id=snippet_input.spdx_id,
                                                   parent_id=document_fixture().creation_info.spdx_id,
                                                   element_type=SpdxElementType.SNIPPET,
                                                   full_element=snippet_input))

    assert validation_messages == [expected]
