from typing import List

import pytest

from src.model.document import Document
from src.model.license_expression import LicenseExpression
from src.model.snippet import Snippet
from src.model.spdx_no_assertion import SpdxNoAssertion
from src.validation.snippet_validator import SnippetValidator
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.valid_defaults import get_snippet, get_document, get_file


def test_valid_snippet():
    document: Document = get_document(files=[get_file(spdx_id="SPDXRef-File")])

    snippet_validator = SnippetValidator("2.3", document)

    snippet = Snippet("SPDXRef-Snippet", "SPDXRef-File", (200, 400), (20, 40), LicenseExpression("some_license"),
                      SpdxNoAssertion(), "comment on license",
                      "copyright", "comment", "name", ["attribution"])
    validation_messages: List[ValidationMessage] = snippet_validator.validate_snippet(snippet)

    assert validation_messages == []


@pytest.mark.parametrize("snippet_id, snippet_file_id, file_id, expected_message",
                         [("SPDXRef-some_snippet", "SPDXRef-File", "SPDXRef-File",
                           'spdx_id must only contain letters, numbers, "." and "-" and must begin with "SPDXRef-", but is: SPDXRef-some_snippet'),
                          ("SPDXRef-Snippet", "SPDXRef-some_file", "SPDXRef-some_file",
                           'spdx_id must only contain letters, numbers, "." and "-" and must begin with "SPDXRef-", but is: SPDXRef-some_file'),
                          ("SPDXRef-Snippet", "SPDXRef-File", "SPDXRef-hiddenFile",
                           "did not find the referenced spdx_id SPDXRef-File in the SPDX document's files")
                          ])
def test_invalid_spdx_ids(snippet_id, snippet_file_id, file_id, expected_message):
    snippet_validator = SnippetValidator("2.3", get_document(files=[get_file(spdx_id=file_id)]))
    snippet = get_snippet(spdx_id=snippet_id, file_spdx_id=snippet_file_id)
    validation_messages: List[ValidationMessage] = snippet_validator.validate_snippet(snippet)

    expected = ValidationMessage(expected_message,
                                 ValidationContext(spdx_id=snippet_id, element_type=SpdxElementType.SNIPPET,
                                                   full_element=snippet))

    assert validation_messages == [expected]


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
    snippet_validator = SnippetValidator("2.3", get_document(files=[get_file()]))

    validation_messages: List[ValidationMessage] = snippet_validator.validate_snippet(snippet_input)

    expected = ValidationMessage(expected_message,
                                 ValidationContext(spdx_id=snippet_input.spdx_id, element_type=SpdxElementType.SNIPPET,
                                                   full_element=snippet_input))

    assert validation_messages == [expected]
