from typing import List

from src.model.snippet import Snippet
from src.model.spdx_no_assertion import SpdxNoAssertion
from src.model.spdx_none import SpdxNone
from src.validation.snippet_validator import SnippetValidator
from src.validation.validation_message import ValidationMessage


def test_correct_snippet():
    snippet_validator = SnippetValidator("2.3")

    snippet = Snippet("id", "file_id", (200, 400), (20, 40), SpdxNone(), SpdxNoAssertion(), "comment on license",
                      "copyright", "comment", "name", ["attribution"])
    validation_messages: List[ValidationMessage] = snippet_validator.validate_snippet(snippet)

    assert validation_messages == []
