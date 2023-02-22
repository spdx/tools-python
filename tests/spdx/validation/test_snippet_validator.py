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
from unittest import TestCase

import pytest

from spdx.validation.snippet_validator import validate_snippet_within_document, validate_snippet
from spdx.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.spdx.fixtures import document_fixture, snippet_fixture


def test_valid_snippet():
    snippet = snippet_fixture()
    validation_messages: List[ValidationMessage] = validate_snippet_within_document(snippet, "SPDX-2.3",
                                                                                    document_fixture())

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
    validation_messages: List[ValidationMessage] = validate_snippet_within_document(snippet_input, "SPDX-2.3",
                                                                                    document_fixture())

    expected = ValidationMessage(expected_message,
                                 ValidationContext(spdx_id=snippet_input.spdx_id,
                                                   parent_id=document_fixture().creation_info.spdx_id,
                                                   element_type=SpdxElementType.SNIPPET,
                                                   full_element=snippet_input))

    assert validation_messages == [expected]


def test_v2_2mandatory_fields():
    snippet = snippet_fixture(license_concluded=None, copyright_text=None)

    assert validate_snippet(snippet, "SPDX-2.3") == []

    validation_messages: List[ValidationMessage] = validate_snippet(snippet, "SPDX-2.2")

    context = ValidationContext(spdx_id=snippet.spdx_id, element_type=SpdxElementType.SNIPPET, full_element=snippet)
    mandatory_fields = ["license_concluded", "copyright_text"]
    expected = [ValidationMessage(f"{field} is mandatory in SPDX-2.2", context) for field in mandatory_fields]

    TestCase().assertCountEqual(validation_messages, expected)
