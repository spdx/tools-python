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

from spdx.validation.creation_info_validator import validate_creation_info
from spdx.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.spdx.fixtures import creation_info_fixture


def test_valid_creation_info():
    creation_info = creation_info_fixture()
    validation_messages: List[ValidationMessage] = validate_creation_info(creation_info, "SPDX-2.3")

    assert validation_messages == []


@pytest.mark.parametrize \
        ("creation_info_input, spdx_id, expected_message",
         [(creation_info_fixture(spdx_id="SPDXRef-doc"), "SPDXRef-doc",
           'spdx_id must be "SPDXRef-DOCUMENT", but is: SPDXRef-doc'),
          (creation_info_fixture(data_license="MIT"), "SPDXRef-DOCUMENT",
           'data_license must be "CC0-1.0", but is: MIT'),
          (creation_info_fixture(document_namespace="some_namespace"), "SPDXRef-DOCUMENT",
           "document_namespace must be a valid URI specified in RFC-3986 and must contain no fragment (#), but is: some_namespace"),
          ])
def test_invalid_creation_info(creation_info_input, expected_message, spdx_id):
    validation_messages: List[ValidationMessage] = validate_creation_info(creation_info_input, "SPDX-2.3")

    expected = ValidationMessage(expected_message, ValidationContext(spdx_id, None, SpdxElementType.DOCUMENT))

    assert validation_messages == [expected]
