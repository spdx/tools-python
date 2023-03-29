# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from datetime import datetime

import pytest

from spdx.model.annotation import AnnotationType
from spdx.parser.error import SPDXParsingError
from spdx.parser.tagvalue.parser import Parser
from tests.spdx.parser.tagvalue.test_creation_info_parser import DOCUMENT_STR


def test_parse_annotation():
    parser = Parser()
    annotation_str = "\n".join([
        "Annotator: Person: Jane Doe()",
        "AnnotationDate: 2010-01-29T18:30:22Z",
        "AnnotationComment: <text>Document level annotation</text>",
        "AnnotationType: OTHER",
        "SPDXREF: SPDXRef-DOCUMENT"
    ])
    document = parser.parse("\n".join([DOCUMENT_STR, annotation_str]))
    assert document is not None
    assert len(document.annotations) == 1
    annotation = document.annotations[0]
    assert annotation.annotator.name == "Jane Doe"
    assert annotation.annotation_date == datetime(2010, 1, 29, 18, 30, 22)
    assert annotation.annotation_comment == "Document level annotation"
    assert annotation.annotation_type == AnnotationType.OTHER
    assert annotation.spdx_id == "SPDXRef-DOCUMENT"


@pytest.mark.parametrize("annotation_str, expected_message", [
    ("Annotator: Person: Jane Doe()", r"__init__() missing 4 "
                                      "required positional arguments: 'spdx_id', 'annotation_type', "
                                      "'annotation_date', and 'annotation_comment'"),
    ("Annotator: Person: Jane Doe()\nAnnotationType: SOURCE\nAnnotationDate: 201001-2912:23",
     "Error while parsing Annotation: ['Invalid AnnotationType: SOURCE. Line: 2', "
     "'Error while parsing AnnotationDate: Token did not match specified grammar "
     "rule. Line: 3']"),
    ("Annotator: Jane Doe()\nAnnotationDate: 201001-29T18:30:22Z\n"
     "AnnotationComment: <text>Document level annotation</text>\nAnnotationType: OTHER\nSPDXREF: SPDXRef-DOCUMENT",
     "Error while parsing Annotation: ['Error while parsing Annotator: Token did "
     "not match specified grammar rule. Line: 1', 'Error while parsing "
     "AnnotationDate: Token did not match specified grammar rule. Line: 2']"),
    ("Annotator: Person: ()", "Error while parsing Annotation: [['No name for Person provided: Person: ().']]"),
    ("AnnotationType: REVIEW", "Element Annotation is not the current element in scope, probably the "
                               "expected tag to start the element (Annotator) is missing. Line: 1")])
def test_parse_invalid_annotation(annotation_str, expected_message):
    parser = Parser()
    with pytest.raises(SPDXParsingError) as err:
        parser.parse(annotation_str)

    assert expected_message in err.value.get_messages()[0]
