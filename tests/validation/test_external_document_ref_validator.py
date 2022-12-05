from typing import List
from unittest import mock

from src.model.external_document_ref import ExternalDocumentRef
from src.validation.external_document_ref_validator import ExternalDocumentRefValidator
from src.validation.validation_message import ValidationMessage


@mock.patch('src.model.checksum.Checksum', autospec=True)
def test_correct_external_document_ref(checksum):
    external_document_ref_validator = ExternalDocumentRefValidator("2.3")

    external_document_ref = ExternalDocumentRef("uri", "id", checksum)
    validation_messages: List[ValidationMessage] = external_document_ref_validator.validate_external_document_ref(external_document_ref)

    assert validation_messages == []
