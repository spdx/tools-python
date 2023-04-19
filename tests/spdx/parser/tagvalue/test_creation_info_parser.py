# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime
from unittest import TestCase

import pytest

from spdx_tools.spdx.constants import DOCUMENT_SPDX_ID
from spdx_tools.spdx.model import Actor, ActorType, Checksum, ChecksumAlgorithm, ExternalDocumentRef, Version
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.tagvalue.parser import Parser

DOCUMENT_STR = "\n".join(
    [
        "SPDXVersion: SPDX-2.3",
        "DataLicense: CC0-1.0",
        "DocumentName: Sample_Document-V2.3",
        f"SPDXID: {DOCUMENT_SPDX_ID}",
        "DocumentComment: <text>Sample Comment</text>",
        "DocumentNamespace: https://spdx.org/spdxdocs/spdx-example-444504E0-4F89-41D3-9A0C-0305E82C3301",
        "ExternalDocumentRef: DocumentRef-spdx-tool-1.2 "
        "http://spdx.org/spdxdocs/spdx-tools-v1.2-3F2504E0-4F89-41D3-9A0C-0305E82C3301 "
        "SHA1: d6a770ba38583ed4bb4525bd96e50461655d2759",
        "Creator: Person: Bob (bob@example.com)",
        "Creator: Organization: Acme.",
        "Created: 2010-02-03T00:00:00Z",
        "CreatorComment: <text>Sample Comment \nwith multiple \nlines.</text>",
        "LicenseListVersion: 3.17",
    ]
)


def test_parse_creation_info():
    parser = Parser()
    document = parser.parse(DOCUMENT_STR)
    assert document is not None
    creation_info = document.creation_info
    assert creation_info is not None
    assert creation_info.spdx_version == "SPDX-2.3"
    assert creation_info.data_license == "CC0-1.0"
    assert creation_info.name == "Sample_Document-V2.3"
    assert creation_info.spdx_id == DOCUMENT_SPDX_ID
    assert creation_info.document_comment == "Sample Comment"
    assert (
        creation_info.document_namespace
        == "https://spdx.org/spdxdocs/spdx-example-444504E0-4F89-41D3-9A0C-0305E82C3301"
    )
    TestCase().assertCountEqual(
        creation_info.creators,
        [Actor(ActorType.PERSON, "Bob", "bob@example.com"), Actor(ActorType.ORGANIZATION, "Acme.")],
    )
    assert creation_info.creator_comment == "Sample Comment \nwith multiple \nlines."
    assert creation_info.created == datetime(2010, 2, 3)
    assert creation_info.license_list_version == Version(3, 17)
    assert creation_info.external_document_refs == [
        ExternalDocumentRef(
            "DocumentRef-spdx-tool-1.2",
            "http://spdx.org/spdxdocs/spdx-tools-v1.2-3F2504E0-4F89-41D3-9A0C-0305E82C3301",
            Checksum(ChecksumAlgorithm.SHA1, "d6a770ba38583ed4bb4525bd96e50461655d2759"),
        )
    ]


@pytest.mark.parametrize(
    "document_str, expected_message",
    (
        [
            (
                "\n".join(
                    [
                        "SPDXVersion: SPDX-2.3",
                        "DataLicense: CC0-1.0",
                        "DocumentName: Sample_Document-V2.3",
                        f"SPDXID: {DOCUMENT_SPDX_ID}",
                        "DocumentComment: <text>Sample Comment</text>",
                        "DocumentNamespace: <text>Sample Comment</text>",
                        "ExternalDocumentRef: DocumentRef-spdx-tool-1.2:htp://spdx.org:SHA1: "
                        "d6a770ba38583ed4bb4525bd96e50461655d2759",
                        "Creator: Person Bob (bob@example.com)",
                        "Creator: Organization: Acme [email]",
                        "Created: 2010-02-03T00:00:0Z",
                        "CreatorComment: <text>Sample Comment</text>",
                        "LicenseListVersion: 7",
                    ]
                ),
                (
                    "Error while parsing CreationInfo: ['Error while parsing DocumentNamespace: "
                    "Token did not match specified grammar rule. Line: 6', \"Error while parsing "
                    "ExternalDocumentRef: Couldn't split the first part of the value into "
                    "document_ref_id and document_uri. Line: 7\", 'Error while parsing Creator: "
                    "Token did not match specified grammar rule. Line: 8', 'Error while parsing "
                    "Created: Token did not match specified grammar rule. Line: 10', '7 is not a "
                    "valid version string']"
                ),
            ),
            (
                "\n".join(
                    [
                        "SPDXVersion: SPDX-2.3",
                        "DataLicense: CC0-1.0",
                        "DocumentName: Sample_Document-V2.3",
                        f"SPDXID: {DOCUMENT_SPDX_ID}",
                    ]
                ),
                r"__init__() missing 3 required positional arguments: 'document_namespace', 'creators', and 'created'",
            ),
            (
                "LicenseListVersion: 3.5\nLicenseListVersion: 3.7",
                "Error while parsing CreationInfo: ['Multiple values for LicenseListVersion found. Line: 2']",
            ),
            (
                "ExternalDocumentRef: Document_ref document_uri SHA1: afded",
                "Error while parsing CreationInfo: [\"Error while parsing ExternalDocumentRef: Couldn't match "
                'Checksum. Line: 1"]',
            ),
        ]
    ),
)
def test_parse_invalid_creation_info(document_str, expected_message):
    parser = Parser()
    with pytest.raises(SPDXParsingError) as err:
        parser.parse(document_str)
    assert expected_message in err.value.get_messages()[0]
