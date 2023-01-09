from unittest import mock

import pytest

from spdx.model.external_document_ref import ExternalDocumentRef


@mock.patch('spdx.model.checksum.Checksum', autospec=True)
def test_correct_initialization(checksum):
    external_document_ref = ExternalDocumentRef("id", "uri", checksum)
    assert external_document_ref.document_ref_id == "id"
    assert external_document_ref.document_uri == "uri"
    assert external_document_ref.checksum == checksum


@mock.patch('spdx.model.checksum.Checksum', autospec=True)
def test_wrong_type_in_spdx_id(checksum):
    with pytest.raises(TypeError):
        ExternalDocumentRef(42, "uri", checksum)


@mock.patch('spdx.model.checksum.Checksum', autospec=True)
def test_wrong_type_in_document_uri(checksum):
    with pytest.raises(TypeError):
        ExternalDocumentRef("id", 42, checksum)


def test_wrong_type_in_checksum():
    with pytest.raises(TypeError):
        ExternalDocumentRef("id", "uri", 42)
