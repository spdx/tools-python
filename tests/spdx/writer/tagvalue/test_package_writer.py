# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest.mock import MagicMock, call, mock_open, patch

from spdx.writer.tagvalue.package_writer import write_package
from tests.spdx.fixtures import package_fixture


def test_package_writer():
    package = package_fixture()

    mock: MagicMock = mock_open()
    with patch(f"{__name__}.open", mock, create=True):
        with open("foo", "w") as file:
            write_package(package, file)

    mock.assert_called_once_with("foo", "w")
    handle = mock()
    handle.write.assert_has_calls(
        [
            call("## Package Information\n"),
            call("PackageName: packageName\n"),
            call("SPDXID: SPDXRef-Package\n"),
            call("PackageVersion: 12.2\n"),
            call("PackageFileName: ./packageFileName\n"),
            call("PackageSupplier: Person: supplierName (some@mail.com)\n"),
            call("PackageOriginator: Person: originatorName (some@mail.com)\n"),
            call("PackageDownloadLocation: https://download.com\n"),
            call("FilesAnalyzed: True\n"),
            call("PackageVerificationCode: 85ed0817af83a24ad8da68c2b5094de69833983c (excludes: ./exclude.py)\n"),
            call("PackageChecksum: SHA1: 71c4025dd9897b364f3ebbb42c484ff43d00791c\n"),
            call("PackageHomePage: https://homepage.com\n"),
            call("PackageSourceInfo: sourceInfo\n"),
            call("PackageLicenseConcluded: MIT AND GPL-2.0-only\n"),
            call("PackageLicenseInfoFromFiles: MIT\n"),
            call("PackageLicenseInfoFromFiles: GPL-2.0-only\n"),
            call("PackageLicenseInfoFromFiles: NOASSERTION\n"),
            call("PackageLicenseDeclared: MIT AND GPL-2.0-only\n"),
            call("PackageLicenseComments: packageLicenseComment\n"),
            call("PackageCopyrightText: packageCopyrightText\n"),
            call("PackageSummary: packageSummary\n"),
            call("PackageDescription: packageDescription\n"),
            call("PackageComment: packageComment\n"),
            call("ExternalRef: PACKAGE-MANAGER maven-central org.apache.tomcat:tomcat:9.0.0.M4\n"),
            call("ExternalRefComment: externalPackageRefComment\n"),
            call("PackageAttributionText: packageAttributionText\n"),
            call("PrimaryPackagePurpose: SOURCE\n"),
            call("ReleaseDate: 2022-12-01T00:00:00Z\n"),
            call("BuiltDate: 2022-12-02T00:00:00Z\n"),
            call("ValidUntilDate: 2022-12-03T00:00:00Z\n"),
        ]
    )
