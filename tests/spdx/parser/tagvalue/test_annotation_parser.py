# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime

import pytest

from spdx_tools.spdx.constants import DOCUMENT_SPDX_ID
from spdx_tools.spdx.model import AnnotationType
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.tagvalue.parser import Parser
from tests.spdx.parser.tagvalue.test_creation_info_parser import DOCUMENT_STR


def test_parse_annotation():
    parser = Parser()
    annotation_str = "\n".join(
        [
            "Annotator: Person: Jane Doe()",
            "AnnotationDate: 2010-01-29T18:30:22Z",
            "AnnotationComment: <text>Document level annotation</text>",
            "AnnotationType: OTHER",
            f"SPDXREF: {DOCUMENT_SPDX_ID}",
        ]
    )
    document = parser.parse("\n".join([DOCUMENT_STR, annotation_str]))
    assert document is not None
    assert len(document.annotations) == 1
    annotation = document.annotations[0]
    assert annotation.annotator.name == "Jane Doe"
    assert annotation.annotation_date == datetime(2010, 1, 29, 18, 30, 22)
    assert annotation.annotation_comment == "Document level annotation"
    assert annotation.annotation_type == AnnotationType.OTHER
    assert annotation.spdx_id == DOCUMENT_SPDX_ID


@pytest.mark.parametrize(
    "annotation_str, expected_message",
    [
        (
            "Annotator: Person: Jane Doe()",
            r"__init__() missing 4 "
            "required positional arguments: 'spdx_id', 'annotation_type', "
            "'annotation_date', and 'annotation_comment'",
        ),
        (
            "Annotator: Person: Jane Doe()\nAnnotationType: SOURCE\nAnnotationDate: 201001-2912:23",
            "Error while parsing Annotation: ['Invalid AnnotationType: SOURCE. Line: 2', "
            "'Error while parsing AnnotationDate: Token did not match specified grammar "
            "rule. Line: 3']",
        ),
        (
            "Annotator: Jane Doe()\nAnnotationDate: 201001-29T18:30:22Z\n"
            "AnnotationComment: <text>Document level annotation</text>\nAnnotationType: OTHER\n"
            f"SPDXREF: {DOCUMENT_SPDX_ID}",
            "Error while parsing Annotation: ['Error while parsing Annotator: Token did "
            "not match specified grammar rule. Line: 1', 'Error while parsing "
            "AnnotationDate: Token did not match specified grammar rule. Line: 2']",
        ),
        ("Annotator: Person: ()", "Error while parsing Annotation: [['No name for Actor provided: Person: ().']]"),
        (
            "AnnotationType: REVIEW",
            "Element Annotation is not the current element in scope, probably the "
            "expected tag to start the element (Annotator) is missing. Line: 1",
        ),
    ],
)
def test_parse_invalid_annotation(annotation_str, expected_message):
    parser = Parser()
    with pytest.raises(SPDXParsingError) as err:
        parser.parse(annotation_str)

    assert expected_message in err.value.get_messages()[0]
