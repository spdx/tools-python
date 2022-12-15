from typing import List

from src.model.document import Document
from src.validation.document_validator import DocumentValidator
from src.validation.validation_message import ValidationMessage
from tests.valid_defaults import get_creation_info, get_package, get_file, get_snippet, get_annotation, \
    get_relationship, get_extracted_licensing_info


def test_correct_document():
    document_validator = DocumentValidator("2.3")

    document = Document(get_creation_info(), [get_package(), get_package()], [get_file(), get_file()],
                        [get_snippet(), get_snippet()], [get_annotation(), get_annotation()],
                        [get_relationship(), get_relationship()],
                        [get_extracted_licensing_info(), get_extracted_licensing_info()])
    validation_messages: List[ValidationMessage] = document_validator.validate_full_spdx_document(document)

    assert validation_messages == []

# TODO: some kind of super test is needed to test that all the subvalidations are correctly called
