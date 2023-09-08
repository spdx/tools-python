# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest.mock import MagicMock, call, mock_open, patch

from spdx_tools.spdx.writer.tagvalue.package_writer import write_package
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
            call(f"PackageName: {package.name}\n"),
            call(f"SPDXID: {package.spdx_id}\n"),
            call(f"PackageVersion: {package.version}\n"),
            call(f"PackageFileName: {package.file_name}\n"),
            call(f"PackageSupplier: Person: {package.supplier.name} ({package.supplier.email})\n"),
            call(f"PackageOriginator: Person: {package.originator.name} ({package.originator.email})\n"),
            call(f"PackageDownloadLocation: {package.download_location}\n"),
            call("FilesAnalyzed: true\n"),
            call(f"PackageVerificationCode: {package.verification_code.value} (excludes: ./exclude.py)\n"),
            call("PackageChecksum: SHA1: 71c4025dd9897b364f3ebbb42c484ff43d00791c\n"),
            call(f"PackageHomePage: {package.homepage}\n"),
            call(f"PackageSourceInfo: {package.source_info}\n"),
            call(f"PackageLicenseConcluded: {package.license_concluded}\n"),
            call(f"PackageLicenseInfoFromFiles: {package.license_info_from_files[0]}\n"),
            call(f"PackageLicenseInfoFromFiles: {package.license_info_from_files[1]}\n"),
            call(f"PackageLicenseInfoFromFiles: {package.license_info_from_files[2]}\n"),
            call(f"PackageLicenseDeclared: {package.license_declared}\n"),
            call(f"PackageLicenseComments: {package.license_comment}\n"),
            call(f"PackageCopyrightText: {package.copyright_text}\n"),
            call(f"PackageSummary: {package.summary}\n"),
            call(f"PackageDescription: {package.description}\n"),
            call(f"PackageComment: {package.comment}\n"),
            call(
                f"ExternalRef: PACKAGE-MANAGER {package.external_references[0].reference_type} "
                f"{package.external_references[0].locator}\n"
            ),
            call(f"ExternalRefComment: {package.external_references[0].comment}\n"),
            call(f"PackageAttributionText: {package.attribution_texts[0]}\n"),
            call(f"PrimaryPackagePurpose: {package.primary_package_purpose.name}\n"),
            call("ReleaseDate: 2022-11-01T00:00:00Z\n"),
            call("BuiltDate: 2022-11-02T00:00:00Z\n"),
            call("ValidUntilDate: 2022-11-03T00:00:00Z\n"),
        ]
    )
