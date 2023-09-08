# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

import os
from datetime import datetime
from unittest.mock import MagicMock, call, mock_open, patch

import pytest

from spdx_tools.spdx.model import (
    Actor,
    ActorType,
    Checksum,
    ChecksumAlgorithm,
    CreationInfo,
    Document,
    File,
    Package,
    Relationship,
    RelationshipType,
    Snippet,
)
from spdx_tools.spdx.parser.tagvalue import tagvalue_parser
from spdx_tools.spdx.writer.tagvalue.tagvalue_writer import write_document, write_document_to_file
from tests.spdx.fixtures import checksum_fixture, document_fixture


@pytest.fixture
def temporary_file_path() -> str:
    temporary_file_path = "temp_test_tag_value_writer_output.spdx"
    yield temporary_file_path
    os.remove(temporary_file_path)


def test_write_tag_value(temporary_file_path: str):
    document = document_fixture()

    write_document_to_file(document, temporary_file_path, False)

    parsed_document = tagvalue_parser.parse_from_file(temporary_file_path)

    assert parsed_document == document


def test_correct_order_of_elements():
    packages = [
        Package(name="Test Package A", spdx_id="SPDXRef-Package-A", download_location=""),
        Package(name="Test Package B", spdx_id="SPDXRef-Package-B", download_location=""),
    ]
    files = [
        File(name="Test File A", spdx_id="SPDXRef-File-A", checksums=[checksum_fixture()]),
        File(name="Test File B", spdx_id="SPDXRef-File-B", checksums=[checksum_fixture()]),
    ]
    snippets = [
        Snippet(spdx_id="SPDXRef-Snippet-A", file_spdx_id="DocumentRef-External:SPDXRef-File", byte_range=(1, 2)),
        Snippet(spdx_id="SPDXRef-Snippet-B", file_spdx_id="SPDXRef-File-A", byte_range=(1, 2)),
        Snippet(spdx_id="SPDXRef-Snippet-C", file_spdx_id="SPDXRef-File-B", byte_range=(3, 4)),
    ]
    relationships = [Relationship("SPDXRef-Package-A", RelationshipType.CONTAINS, "SPDXRef-File-B")]
    document = document_fixture(
        files=files,
        packages=packages,
        snippets=snippets,
        relationships=relationships,
        annotations=[],
        extracted_licensing_info=[],
    )

    mock: MagicMock = mock_open()
    with patch(f"{__name__}.open", mock, create=True):
        with open("foo", "w") as file:
            write_document(document, file)

    mock.assert_called_once_with("foo", "w")
    handle = mock()
    handle.write.assert_has_calls(
        [
            call("## Document Information\n"),
            call("SPDXVersion: SPDX-2.3\n"),
            call("DataLicense: CC0-1.0\n"),
            call("SPDXID: SPDXRef-DOCUMENT\n"),
            call("DocumentName: documentName\n"),
            call("DocumentNamespace: https://some.namespace\n"),
            call("DocumentComment: documentComment\n"),
            call("\n## External Document References\n"),
            call(
                "ExternalDocumentRef: DocumentRef-external https://namespace.com "
                "SHA1: 71c4025dd9897b364f3ebbb42c484ff43d00791c\n"
            ),
            call("\n"),
            call("## Creation Information\n"),
            call("LicenseListVersion: 3.19\n"),
            call("Creator: Person: creatorName (some@mail.com)\n"),
            call("Created: 2022-12-01T00:00:00Z\n"),
            call("CreatorComment: creatorComment\n"),
            call("\n"),
            call("## Snippet Information\n"),
            call("SnippetSPDXID: SPDXRef-Snippet-A\n"),
            call("SnippetFromFileSPDXID: DocumentRef-External:SPDXRef-File\n"),
            call("SnippetByteRange: 1:2\n"),
            call("\n"),
            call("## File Information\n"),
            call("FileName: Test File A\n"),
            call("SPDXID: SPDXRef-File-A\n"),
            call("FileChecksum: SHA1: 71c4025dd9897b364f3ebbb42c484ff43d00791c\n"),
            call("\n"),
            call("## Snippet Information\n"),
            call("SnippetSPDXID: SPDXRef-Snippet-B\n"),
            call("SnippetFromFileSPDXID: SPDXRef-File-A\n"),
            call("SnippetByteRange: 1:2\n"),
            call("\n"),
            call("## Package Information\n"),
            call("PackageName: Test Package A\n"),
            call("SPDXID: SPDXRef-Package-A\n"),
            call("PackageDownloadLocation: \n"),
            call("FilesAnalyzed: true\n"),
            call("\n"),
            call("## File Information\n"),
            call("FileName: Test File B\n"),
            call("SPDXID: SPDXRef-File-B\n"),
            call("FileChecksum: SHA1: 71c4025dd9897b364f3ebbb42c484ff43d00791c\n"),
            call("\n"),
            call("## Snippet Information\n"),
            call("SnippetSPDXID: SPDXRef-Snippet-C\n"),
            call("SnippetFromFileSPDXID: SPDXRef-File-B\n"),
            call("SnippetByteRange: 3:4\n"),
            call("\n"),
            call("## Package Information\n"),
            call("PackageName: Test Package B\n"),
            call("SPDXID: SPDXRef-Package-B\n"),
            call("PackageDownloadLocation: \n"),
            call("FilesAnalyzed: true\n"),
            call("\n"),
            call("\n"),
        ]
    )


def test_same_file_in_multiple_packages():
    creation_info = CreationInfo(
        spdx_version="SPDX-2.3",
        spdx_id="SPDXRef-DOCUMENT",
        data_license="CC0-1.0",
        name="SPDX Lite Document",
        document_namespace="https://test.namespace.com",
        creators=[Actor(ActorType.PERSON, "John Doe")],
        created=datetime(2023, 3, 14, 8, 49),
    )
    package_a = Package(
        name="Example package A",
        spdx_id="SPDXRef-Package-A",
        download_location="https://download.com",
    )
    package_b = Package(
        name="Example package B",
        spdx_id="SPDXRef-Package-B",
        download_location="https://download.com",
    )
    file = File(
        name="Example file",
        spdx_id="SPDXRef-File",
        checksums=[Checksum(ChecksumAlgorithm.SHA1, "2fd4e1c67a2d28fced849ee1bb76e7391b93eb12")],
    )

    relationships = [
        Relationship("SPDXRef-DOCUMENT", RelationshipType.DESCRIBES, "SPDXRef-Package-A"),
        Relationship("SPDXRef-DOCUMENT", RelationshipType.DESCRIBES, "SPDXRef-Package-B"),
        Relationship("SPDXRef-Package-A", RelationshipType.CONTAINS, "SPDXRef-File"),
        Relationship("SPDXRef-Package-B", RelationshipType.CONTAINS, "SPDXRef-File"),
    ]
    document = Document(
        creation_info=creation_info,
        packages=[package_a, package_b],
        files=[file],
        relationships=relationships,
    )
    mock: MagicMock = mock_open()
    with patch(f"{__name__}.open", mock, create=True):
        with open("foo", "w") as file:
            write_document(document, file)

    mock.assert_called_once_with("foo", "w")
    handle = mock()
    handle.write.assert_has_calls(
        [
            call("## Document Information\n"),
            call("SPDXVersion: SPDX-2.3\n"),
            call("DataLicense: CC0-1.0\n"),
            call("SPDXID: SPDXRef-DOCUMENT\n"),
            call("DocumentName: SPDX Lite Document\n"),
            call("DocumentNamespace: https://test.namespace.com\n"),
            call("\n"),
            call("## Creation Information\n"),
            call("Creator: Person: John Doe\n"),
            call("Created: 2023-03-14T08:49:00Z\n"),
            call("\n"),
            call("## Package Information\n"),
            call("PackageName: Example package A\n"),
            call("SPDXID: SPDXRef-Package-A\n"),
            call("PackageDownloadLocation: https://download.com\n"),
            call("FilesAnalyzed: true\n"),
            call("\n"),
            call("## File Information\n"),
            call("FileName: Example file\n"),
            call("SPDXID: SPDXRef-File\n"),
            call("FileChecksum: SHA1: 2fd4e1c67a2d28fced849ee1bb76e7391b93eb12\n"),
            call("\n"),
            call("## Package Information\n"),
            call("PackageName: Example package B\n"),
            call("SPDXID: SPDXRef-Package-B\n"),
            call("PackageDownloadLocation: https://download.com\n"),
            call("FilesAnalyzed: true\n"),
            call("\n"),
            call("## Relationships\n"),
            call("Relationship: SPDXRef-DOCUMENT DESCRIBES SPDXRef-Package-A\n"),
            call("Relationship: SPDXRef-DOCUMENT DESCRIBES SPDXRef-Package-B\n"),
            call("Relationship: SPDXRef-Package-B CONTAINS SPDXRef-File\n"),
            call("\n"),
        ]
    )
