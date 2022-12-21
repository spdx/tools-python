from typing import List

from src.model.document import Document
from src.validation.document_validator import validate_full_spdx_document
from src.validation.validation_message import ValidationMessage
from tests.valid_defaults import get_creation_info, get_package, get_file, get_snippet, get_annotation, \
    get_relationship, get_extracted_licensing_info


def test_valid_document():
    document = Document(get_creation_info(), [get_package(), get_package()], [get_file(), get_file()],
                        [get_snippet(), get_snippet()], [get_annotation(), get_annotation()],
                        [get_relationship(), get_relationship()],
                        [get_extracted_licensing_info(), get_extracted_licensing_info()])
    validation_messages: List[ValidationMessage] = validate_full_spdx_document(document, "2.3")

    assert validation_messages == []

# TODO: https://github.com/spdx/tools-python/issues/375
