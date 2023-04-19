# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import TestCase

import pytest

from spdx_tools.spdx.constants import DOCUMENT_SPDX_ID
from spdx_tools.spdx.validation.spdx_id_validators import (
    get_list_of_all_spdx_ids,
    is_external_doc_ref_present_in_document,
    is_spdx_id_present_in_document,
    is_valid_external_doc_ref_id,
    is_valid_internal_spdx_id,
    validate_spdx_id,
)
from tests.spdx.fixtures import (
    creation_info_fixture,
    document_fixture,
    external_document_ref_fixture,
    file_fixture,
    package_fixture,
    snippet_fixture,
)

DOCUMENT = document_fixture(
    files=[file_fixture(spdx_id="SPDXRef-File1"), file_fixture(spdx_id="SPDXRef-File2")],
    packages=[package_fixture(spdx_id="SPDXRef-Package1"), package_fixture(spdx_id="SPDXRef-Package2")],
    snippets=[snippet_fixture(spdx_id="SPDXRef-Snippet1"), snippet_fixture(spdx_id="SPDXRef-Snippet2")],
    creation_info=creation_info_fixture(
        external_document_refs=[
            external_document_ref_fixture(document_ref_id="DocumentRef-external"),
            external_document_ref_fixture(document_ref_id="DocumentRef-1.2-ext"),
        ]
    ),
)


@pytest.mark.parametrize("spdx_id", [DOCUMENT_SPDX_ID, "SPDXRef-File1", "SPDXRef-1.3-3.7"])
def test_valid_internal_spdx_ids(spdx_id):
    assert is_valid_internal_spdx_id(spdx_id)


@pytest.mark.parametrize(
    "spdx_id", ["spdxId", "spdxRef-DOCUMENT", "SPDXRef.File", "SPDXRef#Snippet", "SPDXRef-1.3_3.7"]
)
def test_invalid_internal_spdx_ids(spdx_id):
    assert not is_valid_internal_spdx_id(spdx_id)


@pytest.mark.parametrize("doc_ref_id", ["DocumentRef-external", "DocumentRef-...+", "DocumentRef-v0.4.2-alpha"])
def test_valid_external_doc_ref_ids(doc_ref_id):
    assert is_valid_external_doc_ref_id(doc_ref_id)


@pytest.mark.parametrize(
    "doc_ref_id", ["external-ref", "Documentref-external", "DocumentRef-...#", "DocumentRef-v0_4_2-alpha"]
)
def test_invalid_external_doc_ref_ids(doc_ref_id):
    assert not is_valid_external_doc_ref_id(doc_ref_id)


def test_is_spdx_id_present_in_document():
    assert is_spdx_id_present_in_document("SPDXRef-File1", DOCUMENT)
    assert is_spdx_id_present_in_document("SPDXRef-Package2", DOCUMENT)
    assert is_spdx_id_present_in_document("SPDXRef-Snippet1", DOCUMENT)
    assert is_spdx_id_present_in_document(DOCUMENT_SPDX_ID, DOCUMENT)
    assert not is_spdx_id_present_in_document("SPDXRef-file2", DOCUMENT)


def test_is_external_doc_ref_present_in_document():
    assert is_external_doc_ref_present_in_document("DocumentRef-1.2-ext", DOCUMENT)
    assert not is_external_doc_ref_present_in_document("DocumentRef-External1", DOCUMENT)


def test_list_of_all_spdx_ids():
    TestCase().assertCountEqual(
        get_list_of_all_spdx_ids(DOCUMENT),
        [
            DOCUMENT_SPDX_ID,
            "SPDXRef-File1",
            "SPDXRef-File2",
            "SPDXRef-Package1",
            "SPDXRef-Package2",
            "SPDXRef-Snippet1",
            "SPDXRef-Snippet2",
        ],
    )


@pytest.mark.parametrize("spdx_id", ["DocumentRef-external:SPDXRef-File", "SPDXRef-Package"])
def test_valid_spdx_id(spdx_id):
    validation_messages = validate_spdx_id(spdx_id, DOCUMENT)

    assert validation_messages == []


@pytest.mark.parametrize(
    "spdx_id, expected_messages",
    [
        (
            "DocumentRef-external:extern:SPDXRef-File",
            [
                "spdx_id must not contain more than one colon in order to separate the external document reference id"
                " from the internal SPDX id, but is: DocumentRef-external:extern:SPDXRef-File"
            ],
        ),
        (
            "DocumentRef external:SPDXRef-File",
            [
                'the external document reference part of spdx_id must only contain letters, numbers, ".", "-" and "+" '
                'and must begin with "DocumentRef-", but is: DocumentRef external',
                'did not find the external document reference "DocumentRef external" in the SPDX document',
            ],
        ),
        (
            "DocRef-ext:SPDXRef-File_2",
            [
                'the external document reference part of spdx_id must only contain letters, numbers, ".", "-" and "+" '
                'and must begin with "DocumentRef-", but is: DocRef-ext',
                'the internal SPDX id part of spdx_id must only contain letters, numbers, "." and "-" and must begin '
                'with "SPDXRef-", but is: SPDXRef-File_2',
                'did not find the external document reference "DocRef-ext" in the SPDX document',
            ],
        ),
        (
            "DocumentRef-external:SPDXRef-File_2",
            [
                'the internal SPDX id part of spdx_id must only contain letters, numbers, "." and "-" and must begin '
                'with "SPDXRef-", but is: SPDXRef-File_2'
            ],
        ),
        (
            "SPDXRef-42+",
            [
                'spdx_id must only contain letters, numbers, "." and "-" and must begin with "SPDXRef-", but is: '
                "SPDXRef-42+"
            ],
        ),
    ],
)
def test_invalid_spdx_id(spdx_id, expected_messages):
    validation_messages = validate_spdx_id(spdx_id, DOCUMENT)

    TestCase().assertCountEqual(validation_messages, expected_messages)


@pytest.mark.parametrize(
    "spdx_id",
    ["DocumentRef-external:SPDXRef-File", DOCUMENT_SPDX_ID, "SPDXRef-File1", "SPDXRef-Package1", "SPDXRef-Snippet1"],
)
def test_valid_spdx_id_with_check_document(spdx_id):
    validation_messages = validate_spdx_id(spdx_id, DOCUMENT, check_document=True)
    assert validation_messages == []


def test_invalid_spdx_id_with_check_document():
    validation_messages = validate_spdx_id("SPDXRef-Filet", DOCUMENT, check_document=True)
    assert validation_messages == ['did not find the referenced spdx_id "SPDXRef-Filet" in the SPDX document']


@pytest.mark.parametrize("spdx_id", ["DocumentRef-external:SPDXRef-File", "SPDXRef-File1"])
def test_valid_spdx_id_with_check_files(spdx_id):
    validation_messages = validate_spdx_id(spdx_id, DOCUMENT, check_files=True)
    assert validation_messages == []


def test_invalid_spdx_id_with_check_files():
    validation_messages = validate_spdx_id("SPDXRef-Package1", DOCUMENT, check_files=True)
    assert validation_messages == [
        'did not find the referenced spdx_id "SPDXRef-Package1" in the SPDX document\'s files'
    ]
