from typing import List

import pytest

from src.model.external_document_ref import ExternalDocumentRef
from src.validation.external_document_ref_validator import validate_external_document_ref
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.valid_defaults import get_checksum, get_external_document_ref


def test_valid_external_document_ref():

    external_document_ref = ExternalDocumentRef("DocumentRef-id", "http://some.uri", get_checksum())
    validation_messages: List[ValidationMessage] = validate_external_document_ref(external_document_ref, "parent_id")

    assert validation_messages == []
