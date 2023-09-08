# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime
from unittest import TestCase

import pytest

from spdx_tools.common.spdx_licensing import spdx_licensing
from spdx_tools.spdx.constants import DOCUMENT_SPDX_ID
from spdx_tools.spdx.model import ExternalPackageRef, ExternalPackageRefCategory, PackagePurpose, SpdxNone
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.tagvalue.parser import Parser
from tests.spdx.parser.tagvalue.test_creation_info_parser import DOCUMENT_STR


def test_parse_package():
    parser = Parser()
    package_str = "\n".join(
        [
            "PackageName: Test",
            "SPDXID: SPDXRef-Package",
            "PackageVersion: 1:22.36.1-8+deb11u1",
            "PackageDownloadLocation: http://example.com/test",
            "FilesAnalyzed: true",
            "PackageSummary: <text>Test package</text>",
            "PackageSourceInfo: <text>Version 1.0 of test</text>",
            "PackageFileName: test-1.0.zip",
            "PackageSupplier: Organization:ACME",
            "PackageOriginator: Organization:ACME",
            "PackageChecksum: SHA1: 2fd4e1c67a2d28fced849ee1bb76e7391b93eb12",
            "PackageVerificationCode: 4e3211c67a2d28fced849ee1bb76e7391b93feba (something.rdf, something.txt)",
            "PackageDescription: <text>A package.</text>",
            "PackageComment: <text>Comment on the package.</text>",
            "PackageCopyrightText: <text> Copyright 2014 Acme Inc.</text>",
            "PackageLicenseDeclared: Apache-2.0",
            "PackageLicenseConcluded: (LicenseRef-2.0 and Apache-2.0)",
            "PackageLicenseInfoFromFiles: Apache-1.0",
            "PackageLicenseInfoFromFiles: Apache-2.0",
            "PackageLicenseInfoFromFiles: NONE",
            "PackageLicenseComments: <text>License Comments</text>",
            "ExternalRef: SECURITY cpe23Type cpe:2.3:a:pivotal_software:spring_framework:4.1.0:*:*:*:*:*:*:",
            "ExternalRefComment: <text>Some comment about the package.</text>",
            "ExternalRef: OTHER LocationRef-acmeforge acmecorp/acmenator/4.1.3-alpha",
            "PrimaryPackagePurpose: OPERATING-SYSTEM",
            "BuiltDate: 2020-01-01T12:00:00Z",
            "ReleaseDate: 2021-01-01T12:00:00Z",
            "ValidUntilDate: 2022-01-01T12:00:00Z",
        ]
    )
    document = parser.parse("\n".join([DOCUMENT_STR, package_str]))
    assert document is not None
    package = document.packages[0]
    assert package.name == "Test"
    assert package.spdx_id == "SPDXRef-Package"
    assert package.version == "1:22.36.1-8+deb11u1"
    assert len(package.license_info_from_files) == 3
    TestCase().assertCountEqual(
        package.license_info_from_files,
        [spdx_licensing.parse("Apache-1.0"), spdx_licensing.parse("Apache-2.0"), SpdxNone()],
    )
    assert package.license_concluded == spdx_licensing.parse("LicenseRef-2.0 AND Apache-2.0")
    assert package.files_analyzed is True
    assert package.comment == "Comment on the package."
    assert len(package.external_references) == 2
    TestCase().assertCountEqual(
        package.external_references,
        [
            ExternalPackageRef(
                ExternalPackageRefCategory.SECURITY,
                "cpe23Type",
                "cpe:2.3:a:pivotal_software:spring_framework:4.1.0:*:*:*:*:*:*:",
                "Some comment about the package.",
            ),
            ExternalPackageRef(
                ExternalPackageRefCategory.OTHER, "LocationRef-acmeforge", "acmecorp/acmenator/4.1.3-alpha"
            ),
        ],
    )
    assert package.primary_package_purpose == PackagePurpose.OPERATING_SYSTEM
    assert package.built_date == datetime(2020, 1, 1, 12)
    assert package.release_date == datetime(2021, 1, 1, 12)
    assert package.valid_until_date == datetime(2022, 1, 1, 12)


@pytest.mark.parametrize(
    "package_str, expected_message",
    [
        (
            "PackageDownloadLocation: SPDXRef-Package",
            "Element Package is not the current element in scope, probably the expected "
            "tag to start the element (PackageName) is missing. Line: 1",
        ),
        (
            "PackageName: TestPackage",
            r"__init__() missing 2 required positional arguments: 'spdx_id' and 'download_location'",
        ),
        (
            "PackageName: TestPackage\nPackageCopyrightText:This is a copyright\n"
            "PackageCopyrightText:MultipleCopyright",
            "Error while parsing Package: ['Multiple values for PackageCopyrightText " "found. Line: 3']",
        ),
        (
            "PackageName: TestPackage\nExternalRef: reference locator",
            (
                "Error while parsing Package: [\"Couldn't split PackageExternalRef in category, "
                'reference_type and locator. Line: 2"]'
            ),
        ),
        (
            "PackageName: TestPackage\nExternalRef: category reference locator",
            "Error while parsing Package: ['Invalid ExternalPackageRefCategory: " "category. Line: 2']",
        ),
        (
            f"SPDXID:{DOCUMENT_SPDX_ID}\nPackageName: TestPackage\nSPDXID:SPDXRef-Package\n"
            "PackageDownloadLocation: download.com\nPackageVerificationCode: category reference locator",
            "Error while parsing Package: ['Error while parsing PackageVerificationCode: "
            "Value did not match expected format. Line: 5']",
        ),
        (
            "PackageName: TestPackage\nBuiltDate: 2012\nValidUntilDate:202-11-02T00:00",
            "Error while parsing Package: ['Error while parsing BuiltDate: Token did not "
            "match specified grammar rule. Line: 2', 'Error while parsing "
            "ValidUntilDate: Token did not match specified grammar rule. Line: 3']",
        ),
        (
            f"SPDXID:{DOCUMENT_SPDX_ID}\nPackageName: TestPackage\nSPDXID:SPDXRef-Package\n"
            "PackageDownloadLocation: download.com\nFilesAnalyzed: FALSE",
            "Error while parsing Package: "
            '[\'The value of FilesAnalyzed must be either "true" or "false", but is: FALSE\']',
        ),
    ],
)
def test_parse_invalid_package(package_str, expected_message):
    parser = Parser()

    with pytest.raises(SPDXParsingError) as err:
        parser.parse(package_str)

    assert expected_message in err.value.get_messages()[0]
