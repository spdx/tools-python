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

from spdx.model.annotation import Annotation
from spdx.model.document import Document
from spdx.validation.annotation_validator import validate_annotation
from spdx.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.spdx.fixtures import document_fixture, annotation_fixture, file_fixture


def test_valid_annotation():
    validation_messages: List[ValidationMessage] = validate_annotation(annotation_fixture(), document_fixture())

    assert validation_messages == []


@pytest.mark.parametrize("annotation_id, file_id, expected_message",
                         [("SPDXRef-File", "SPDXRef-hiddenFile",
                           'did not find the referenced spdx_id "SPDXRef-File" in the SPDX document')
                          ])
def test_invalid_annotation(annotation_id, file_id, expected_message):
    annotation: Annotation = annotation_fixture(spdx_id=annotation_id)
    document: Document = document_fixture(files=[file_fixture(spdx_id=file_id)])
    validation_messages: List[ValidationMessage] = validate_annotation(annotation, document)

    expected = ValidationMessage(expected_message,
                                 ValidationContext(element_type=SpdxElementType.ANNOTATION,
                                                   full_element=annotation))

    assert validation_messages == [expected]
