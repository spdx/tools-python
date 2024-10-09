# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import TestCase

import pytest

from spdx_tools.spdx.document_utils import (
    create_document_without_duplicates,
    create_list_without_duplicates,
    get_contained_spdx_element_ids,
    get_contained_spdx_elements,
    get_element_from_spdx_id,
)
from spdx_tools.spdx.model import FileType, SpdxNoAssertion, SpdxNone
from tests.spdx.fixtures import (
    actor_fixture,
    checksum_fixture,
    creation_info_fixture,
    document_fixture,
    external_document_ref_fixture,
    external_package_ref_fixture,
    extracted_licensing_info_fixture,
    file_fixture,
    package_fixture,
    snippet_fixture,
)


@pytest.fixture
def variables():
    return document_fixture(), package_fixture(), file_fixture(), snippet_fixture()


def test_contained_element_ids(variables):
    document, package, file, snippet = variables
    element_ids = get_contained_spdx_element_ids(document)
    TestCase().assertCountEqual(element_ids, [package.spdx_id, file.spdx_id, snippet.spdx_id])


def test_get_element_from_spdx_id(variables):
    document, package, file, snippet = variables
    assert get_element_from_spdx_id(document, package.spdx_id) == package
    assert get_element_from_spdx_id(document, file.spdx_id) == file
    assert get_element_from_spdx_id(document, snippet.spdx_id) == snippet
    assert get_element_from_spdx_id(document, "unknown_id") is None


def test_get_contained_spdx_elements(variables):
    document, package, file, snippet = variables
    contained_elements = get_contained_spdx_elements(document)
    assert contained_elements[package.spdx_id] == package
    assert contained_elements[file.spdx_id] == file
    assert contained_elements[snippet.spdx_id] == snippet


def test_create_list_without_duplicates():
    list_with_duplicates = [1, 2, 3, 5, 1, 67, 9, 67]

    list_without_duplicates = create_list_without_duplicates(list_with_duplicates)

    assert list_without_duplicates == [1, 2, 3, 5, 67, 9]


def test_create_document_without_duplicates():
    document = document_fixture(
        creation_info=creation_info_fixture(
            creators=[actor_fixture(name="creatorName"), actor_fixture(name="creatorName")],
            external_document_refs=[external_document_ref_fixture(), external_document_ref_fixture()],
        ),
        packages=[
            package_fixture(
                checksums=[checksum_fixture(), checksum_fixture()],
                license_info_from_files=[SpdxNoAssertion(), SpdxNoAssertion()],
                external_references=[external_package_ref_fixture(), external_package_ref_fixture()],
                attribution_texts=["duplicated text", "duplicated text"],
            )
        ],
        files=[
            file_fixture(
                checksums=[checksum_fixture(), checksum_fixture()],
                file_types=[FileType.TEXT, FileType.TEXT],
                license_info_in_file=[SpdxNoAssertion(), SpdxNoAssertion()],
                contributors=["duplicated contributor", "duplicated contributor"],
                attribution_texts=["duplicated text", "duplicated text"],
            )
        ],
        snippets=[
            snippet_fixture(
                license_info_in_snippet=[SpdxNone(), SpdxNone()],
                attribution_texts=["duplicated text", "duplicated text"],
            )
        ],
        extracted_licensing_info=[
            extracted_licensing_info_fixture(cross_references=["duplicated reference", "duplicated reference"])
        ],
    )
    expected_document = document_fixture(
        creation_info=creation_info_fixture(
            creators=[actor_fixture(name="creatorName")], external_document_refs=[external_document_ref_fixture()]
        ),
        packages=[
            package_fixture(
                checksums=[checksum_fixture()],
                license_info_from_files=[SpdxNoAssertion()],
                external_references=[external_package_ref_fixture()],
                attribution_texts=["duplicated text"],
            )
        ],
        files=[
            file_fixture(
                checksums=[checksum_fixture()],
                file_types=[FileType.TEXT],
                license_info_in_file=[SpdxNoAssertion()],
                contributors=["duplicated contributor"],
                attribution_texts=["duplicated text"],
            )
        ],
        snippets=[snippet_fixture(license_info_in_snippet=[SpdxNone()], attribution_texts=["duplicated text"])],
        extracted_licensing_info=[extracted_licensing_info_fixture(cross_references=["duplicated reference"])],
    )

    document_without_duplicates = create_document_without_duplicates(document)

    assert document_without_duplicates == expected_document
