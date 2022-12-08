from typing import List
import pytest

from src.model.license_expression import LicenseExpression
from src.model.snippet import Snippet
from src.model.spdx_no_assertion import SpdxNoAssertion
from src.model.spdx_none import SpdxNone
from src.validation.snippet_validator import SnippetValidator
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.valid_defaults import get_snippet


def test_correct_snippet():
    snippet_validator = SnippetValidator("2.3")

    snippet = Snippet("SPDXRef-Snippet", "SPDXRef-File", (200, 400), (20, 40), LicenseExpression("some_license"), SpdxNoAssertion(), "comment on license",
                      "copyright", "comment", "name", ["attribution"])
    validation_messages: List[ValidationMessage] = snippet_validator.validate_snippet(snippet)

    assert validation_messages == []
    

@pytest.mark.parametrize("snippet_input, expected_message",
                         [(get_snippet(spdx_id="SPDXRef-some_snippet"),
                           'spdx_id must only contain letters, numbers, "." and "-" and must begin with "SPDXRef-", but is: SPDXRef-some_snippet'),
                          (get_snippet(file_spdx_id="SPDXRef-some_file"),
                           'file_spdx_id must only contain letters, numbers, "." and "-" and must begin with "SPDXRef-", but is: SPDXRef-some_file'),
                          (get_snippet(byte_range=(-12, 45)),
                           'byte_range values must be greater than or equal to 1, but is: (-12, 45)'),
                          (get_snippet(byte_range=(45, 23)),
                           'the first value of byte_range must be less than or equal to the second, but is: (45, 23)'),
                          (get_snippet(line_range=(-12, 45)),
                           'line_range values must be greater than or equal to 1, but is: (-12, 45)'),
                          (get_snippet(line_range=(45, 23)),
                           'the first value of line_range must be less than or equal to the second, but is: (45, 23)')
                          ])
def test_wrong_snippet(snippet_input, expected_message):
    parent_id = "SPDXRef-DOCUMENT"
    snippet_validator = SnippetValidator("2.3")
    snippet = snippet_input
    validation_messages: List[ValidationMessage] = snippet_validator.validate_snippet(snippet)

    expected = ValidationMessage(expected_message,
                                 ValidationContext(parent_id=parent_id, element_type=SpdxElementType.SNIPPET,
                                                   full_element=snippet))

    assert validation_messages == [expected]
