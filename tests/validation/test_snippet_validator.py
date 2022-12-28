from typing import List

import pytest

from src.model.document import Document
from src.model.license_expression import LicenseExpression
from src.model.snippet import Snippet
from src.model.spdx_no_assertion import SpdxNoAssertion
from src.validation.snippet_validator import validate_snippet_within_document
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.valid_defaults import get_snippet, get_document, get_file


def test_valid_snippet():
    document: Document = get_document(files=[get_file(spdx_id="SPDXRef-File")])

    snippet = Snippet("SPDXRef-Snippet", "SPDXRef-File", (200, 400), (20, 40), LicenseExpression("some_license"),
                      SpdxNoAssertion(), "comment on license",
                      "copyright", "comment", "name", ["attribution"])
    validation_messages: List[ValidationMessage] = validate_snippet_within_document(snippet, document)

    assert validation_messages == []


@pytest.mark.parametrize("snippet_input, expected_message",
                         [(get_snippet(byte_range=(-12, 45)),
                           "byte_range values must be greater than or equal to 1, but is: (-12, 45)"),
                          (get_snippet(byte_range=(45, 23)),
                           "the first value of byte_range must be less than or equal to the second, but is: (45, 23)"),
                          (get_snippet(line_range=(-12, 45)),
                           "line_range values must be greater than or equal to 1, but is: (-12, 45)"),
                          (get_snippet(line_range=(45, 23)),
                           "the first value of line_range must be less than or equal to the second, but is: (45, 23)")
                          ])
def test_invalid_ranges(snippet_input, expected_message):
    validation_messages: List[ValidationMessage] = validate_snippet_within_document(snippet_input,
                                                                                    get_document(files=[get_file()]))

    expected = ValidationMessage(expected_message,
                                 ValidationContext(spdx_id=snippet_input.spdx_id,
                                                   parent_id=get_document().creation_info.spdx_id,
                                                   element_type=SpdxElementType.SNIPPET,
                                                   full_element=snippet_input))

    assert validation_messages == [expected]
