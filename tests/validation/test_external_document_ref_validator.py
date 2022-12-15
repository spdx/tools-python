from typing import List

import pytest

from src.model.external_document_ref import ExternalDocumentRef
from src.validation.external_document_ref_validator import ExternalDocumentRefValidator
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.valid_defaults import get_checksum, get_external_document_ref


def test_valid_external_document_ref():
    external_document_ref_validator = ExternalDocumentRefValidator("2.3", "parent_id")

    external_document_ref = ExternalDocumentRef("DocumentRef-id", "http://some.uri", get_checksum())
    validation_messages: List[ValidationMessage] = external_document_ref_validator.validate_external_document_ref(
        external_document_ref)

    assert validation_messages == []
