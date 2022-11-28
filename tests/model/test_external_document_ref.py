from unittest import mock

import pytest

from src.model.external_document_ref import ExternalDocumentRef


@mock.patch('src.model.checksum.Checksum', autospec=True)
def test_correct_initialization(checksum):
    external_document_ref = ExternalDocumentRef("uri", "id", checksum)
    assert external_document_ref.document_uri == "uri"
    assert external_document_ref.spdx_id == "id"
    assert external_document_ref.checksum == checksum


@mock.patch('src.model.checksum.Checksum', autospec=True)
def test_wrong_type_in_document_uri(checksum):
    with pytest.raises(TypeError):
        ExternalDocumentRef(42, "id", checksum)


@mock.patch('src.model.checksum.Checksum', autospec=True)
def test_wrong_type_in_spdx_id(checksum):
    with pytest.raises(TypeError):
        ExternalDocumentRef("uri", 42, checksum)


def test_wrong_type_in_checksum():
    with pytest.raises(TypeError):
        ExternalDocumentRef("uri", "id", 42)
