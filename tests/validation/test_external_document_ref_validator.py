from typing import List

import pytest

from src.model.external_document_ref import ExternalDocumentRef
from src.validation.external_document_ref_validator import ExternalDocumentRefValidator
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.valid_defaults import get_checksum, get_external_document_ref


def test_correct_external_document_ref():
    external_document_ref_validator = ExternalDocumentRefValidator("2.3", "parent_id")

    external_document_ref = ExternalDocumentRef("DocumentRef-id", "http://some.uri", get_checksum())
    validation_messages: List[ValidationMessage] = external_document_ref_validator.validate_external_document_ref(
        external_document_ref)

    assert validation_messages == []


@pytest.mark.parametrize("external_document_ref, expected_message",
                         [(get_external_document_ref(document_ref_id="SPDXRef-id"),
                           'document_ref_id must only contain letters, numbers, ".", "-" and "+" and must begin with "DocumentRef-", but is: SPDXRef-id'),
                          (get_external_document_ref(document_ref_id="DocumentRef-some_id"),
                           'document_ref_id must only contain letters, numbers, ".", "-" and "+" and must begin with "DocumentRef-", but is: DocumentRef-some_id'),
                          (get_external_document_ref(document_uri="some_uri"),
                           'document_uri must be a valid URI specified in RFC-3986, but is: some_uri')
                          ])
def test_wrong_external_document_ref(external_document_ref, expected_message):
    parent_id = "SPDXRef-DOCUMENT"
    external_document_ref_validator = ExternalDocumentRefValidator("2.3", parent_id)
    validation_messages: List[ValidationMessage] = external_document_ref_validator.validate_external_document_ref(
        external_document_ref)

    expected = ValidationMessage(expected_message,
                                 ValidationContext(parent_id=parent_id,
                                                   element_type=SpdxElementType.EXTERNAL_DOCUMENT_REF,
                                                   full_element=external_document_ref))

    assert validation_messages == [expected]
