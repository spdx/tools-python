#  Copyright (c) 2022 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from datetime import datetime
from typing import List

import pytest

from src.model.annotation import Annotation, AnnotationType
from src.model.document import Document
from src.validation.annotation_validator import validate_annotation
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.valid_defaults import get_actor, get_annotation, get_document, get_file


def test_valid_annotation():
    document: Document = get_document(files=[get_file(spdx_id="SPDXRef-File")])

    annotation = Annotation("SPDXRef-File", AnnotationType.OTHER, get_actor(), datetime(2022, 1, 1), "comment")
    validation_messages: List[ValidationMessage] = validate_annotation(annotation, document)

    assert validation_messages == []


@pytest.mark.parametrize("annotation_id, file_id, expected_message",
                         [("SPDXRef-File", "SPDXRef-hiddenFile",
                           "did not find the referenced spdx_id SPDXRef-File in the SPDX document")
                          ])
def test_invalid_annotation(annotation_id, file_id, expected_message):
    annotation: Annotation = get_annotation(spdx_id=annotation_id)
    document: Document = get_document(files=[get_file(spdx_id=file_id)])
    validation_messages: List[ValidationMessage] = validate_annotation(annotation, document)

    expected = ValidationMessage(expected_message,
                                 ValidationContext(element_type=SpdxElementType.ANNOTATION,
                                                   full_element=annotation))

    assert validation_messages == [expected]
