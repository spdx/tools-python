from typing import List
from unittest import mock

from src.model.document import Document
from src.validation.document_validator import DocumentValidator
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


@mock.patch('src.model.document.CreationInfo', autospec=True)
@mock.patch('src.model.external_document_ref.ExternalDocumentRef', autospec=True)
@mock.patch('src.model.package.Package', autospec=True)
@mock.patch('src.model.file.File', autospec=True)
@mock.patch('src.model.snippet.Snippet', autospec=True)
@mock.patch('src.model.annotation.Annotation', autospec=True)
@mock.patch('src.model.relationship.Relationship', autospec=True)
@mock.patch('src.model.extracted_licensing_info.ExtractedLicensingInfo', autospec=True)
def test_correct_document(creation_info, ext_ref, package, file, snippet, annotation, relationship,
                          extracted_lic):
    document_validator = DocumentValidator("2.3")

    document = Document("version", "id", "name", "namespace", creation_info, "data_license", [ext_ref, ext_ref],
                        "comment", [package, package], [file, file], [snippet, snippet], [annotation, annotation],
                        [relationship, relationship], [extracted_lic, extracted_lic])
    validation_messages: List[ValidationMessage] = document_validator.validate_full_spdx_document(document)

    assert validation_messages == []

# TODO: some kind of super test is needed to test that all the subvalidations are correctly called
