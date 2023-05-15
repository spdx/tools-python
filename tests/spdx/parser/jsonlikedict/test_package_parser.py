# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime
from unittest import TestCase

import pytest
from license_expression import Licensing

from spdx_tools.spdx.model import (
    Actor,
    ActorType,
    Checksum,
    ChecksumAlgorithm,
    ExternalPackageRef,
    ExternalPackageRefCategory,
    PackagePurpose,
    PackageVerificationCode,
    SpdxNoAssertion,
    SpdxNone,
)
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.jsonlikedict.dict_parsing_functions import parse_list_of_elements
from spdx_tools.spdx.parser.jsonlikedict.package_parser import PackageParser


@pytest.mark.parametrize(
    "homepage, expected_homepage, download_location, expected_download_location, "
    "copyright_text, expected_copyright_text, originator, expected_originator, supplier, expected_supplier",
    [
        (
            "http://ftp.gnu.org/gnu/glibc",
            "http://ftp.gnu.org/gnu/glibc",
            "NOASSERTION",
            SpdxNoAssertion(),
            "NONE",
            SpdxNone(),
            "Organization: ExampleCodeInspect (contact@example.com)",
            Actor(ActorType.ORGANIZATION, "ExampleCodeInspect", "contact@example.com"),
            "NOASSERTION",
            SpdxNoAssertion(),
        ),
        (
            "NOASSERTION",
            SpdxNoAssertion(),
            "NONE",
            SpdxNone(),
            "Copyright 2008-2010 John Smith",
            "Copyright 2008-2010 John Smith",
            None,
            None,
            None,
            None,
        ),
        (
            "NONE",
            SpdxNone(),
            "http://ftp.gnu.org/gnu/glibc/glibc-ports-2.15.tar.gz",
            "http://ftp.gnu.org/gnu/glibc/glibc-ports-2.15.tar.gz",
            "NOASSERTION",
            SpdxNoAssertion(),
            "NOASSERTION",
            SpdxNoAssertion(),
            "Person: Jane Doe (jane.doe@example.com)",
            Actor(ActorType.PERSON, "Jane Doe", "jane.doe@example.com"),
        ),
    ],
)
def test_parse_package(
    homepage,
    expected_homepage,
    download_location,
    expected_download_location,
    copyright_text,
    expected_copyright_text,
    originator,
    expected_originator,
    supplier,
    expected_supplier,
):
    package_parser = PackageParser()

    package_dict = {
        "SPDXID": "SPDXRef-Package",
        "attributionTexts": [
            "The GNU C Library is free software.  See the file COPYING.LIB for copying conditions, and LICENSES for "
            "notices about a few contributions that require these additional notices to be distributed.  License "
            "copyright years may be listed using range notation, e.g., 1996-2015, indicating that every year in the "
            "range, inclusive, is a copyrightable year that would otherwise be listed individually."
        ],
        "builtDate": "2011-01-29T18:30:22Z",
        "checksums": [
            {"algorithm": "MD5", "checksumValue": "624c1abb3664f4b35547e7c73864ad24"},
            {"algorithm": "SHA1", "checksumValue": "85ed0817af83a24ad8da68c2b5094de69833983c"},
            {
                "algorithm": "SHA256",
                "checksumValue": "11b6d3ee554eedf79299905a98f9b9a04e498210b59f15094c916c91d150efcd",
            },
            {
                "algorithm": "BLAKE2b-384",
                "checksumValue": "aaabd89c926ab525c242e6621f2f5fa73aa4afe3d9e24aed727faaadd6af38b620bdb623dd2b4788b1c8"
                "086984af8706",
            },
        ],
        "comment": "This is a comment.",
        "copyrightText": copyright_text,
        "description": "The GNU C Library defines functions that are specified by the ISO C standard, as well as "
        "additional features specific to POSIX and other derivatives of the Unix operating system, and "
        "extensions specific to GNU systems.",
        "downloadLocation": download_location,
        "externalRefs": [
            {
                "referenceCategory": "SECURITY",
                "referenceLocator": "cpe:2.3:a:pivotal_software:spring_framework:4.1.0:*:*:*:*:*:*:*",
                "referenceType": "cpe23Type",
            },
            {
                "comment": "This is the external ref for Acme",
                "referenceCategory": "OTHER",
                "referenceLocator": "acmecorp/acmenator/4.1.3-alpha",
                "referenceType": "http://spdx.org/spdxdocs/spdx-example-444504E0-4F89-41D3-9A0C-0305E82C3301"
                "#LocationRef-acmeforge",
            },
        ],
        "filesAnalyzed": True,
        "homepage": homepage,
        "licenseComments": "The license for this project changed with the release of version x.y.  The version of the "
        "project included here post-dates the license change.",
        "licenseConcluded": "(LGPL-2.0-only OR LicenseRef-3)",
        "licenseDeclared": "(LGPL-2.0-only AND LicenseRef-3)",
        "licenseInfoFromFiles": ["GPL-2.0-only", "LicenseRef-2", "LicenseRef-1", "NOASSERTION"],
        "name": "glibc",
        "originator": originator,
        "packageFileName": "glibc-2.11.1.tar.gz",
        "packageVerificationCode": {
            "packageVerificationCodeExcludedFiles": ["./package.spdx"],
            "packageVerificationCodeValue": "d6a770ba38583ed4bb4525bd96e50461655d2758",
        },
        "primaryPackagePurpose": "SOURCE",
        "releaseDate": "2012-01-29T18:30:22Z",
        "sourceInfo": "uses glibc-2_11-branch from git://sourceware.org/git/glibc.git.",
        "summary": "GNU C library.",
        "supplier": supplier,
        "validUntilDate": "2014-01-29T18:30:22Z",
        "versionInfo": "2.11.1",
    }

    package = package_parser.parse_package(package_dict)

    assert package.spdx_id == "SPDXRef-Package"
    assert package.name == "glibc"
    assert package.download_location == expected_download_location
    assert package.version == "2.11.1"
    assert package.file_name == "glibc-2.11.1.tar.gz"
    assert package.supplier == expected_supplier
    assert package.originator == expected_originator
    assert package.files_analyzed is True
    assert package.verification_code == PackageVerificationCode(
        value="d6a770ba38583ed4bb4525bd96e50461655d2758", excluded_files=["./package.spdx"]
    )
    assert len(package.checksums) == 4
    TestCase().assertCountEqual(
        package.checksums,
        [
            Checksum(ChecksumAlgorithm.MD5, "624c1abb3664f4b35547e7c73864ad24"),
            Checksum(ChecksumAlgorithm.SHA1, "85ed0817af83a24ad8da68c2b5094de69833983c"),
            Checksum(ChecksumAlgorithm.SHA256, "11b6d3ee554eedf79299905a98f9b9a04e498210b59f15094c916c91d150efcd"),
            Checksum(
                ChecksumAlgorithm.BLAKE2B_384,
                "aaabd89c926ab525c242e6621f2f5fa73aa4afe3d9e24aed727faaadd6af38b620bdb623dd2b4788b1c8086984af8706",
            ),
        ],
    )
    assert package.homepage == expected_homepage
    assert package.source_info == "uses glibc-2_11-branch from git://sourceware.org/git/glibc.git."
    assert package.license_concluded == Licensing().parse("(LGPL-2.0-only OR LicenseRef-3)")
    TestCase().assertCountEqual(
        package.license_info_from_files,
        [
            Licensing().parse("GPL-2.0-only"),
            Licensing().parse("LicenseRef-2"),
            Licensing().parse("LicenseRef-1"),
            SpdxNoAssertion(),
        ],
    )
    assert package.license_declared == Licensing().parse("(LGPL-2.0-only AND LicenseRef-3)")
    assert (
        package.license_comment
        == "The license for this project changed with the release of version x.y.  The version of the project included"
        " here post-dates the license change."
    )
    assert package.copyright_text == expected_copyright_text
    assert package.summary == "GNU C library."
    assert (
        package.description
        == "The GNU C Library defines functions that are specified by the ISO C standard, as well as additional "
        "features specific to POSIX and other derivatives of the Unix operating system, and extensions specific "
        "to GNU systems."
    )
    assert package.comment == "This is a comment."
    assert len(package.external_references) == 2
    TestCase().assertCountEqual(
        package.external_references,
        [
            ExternalPackageRef(
                ExternalPackageRefCategory.SECURITY,
                "cpe23Type",
                "cpe:2.3:a:pivotal_software:spring_framework:4.1.0:*:*:*:*:*:*:*",
            ),
            ExternalPackageRef(
                ExternalPackageRefCategory.OTHER,
                "http://spdx.org/spdxdocs/spdx-example-444504E0-4F89-41D3-9A0C-0305E82C3301#LocationRef-acmeforge",
                locator="acmecorp/acmenator/4.1.3-alpha",
                comment="This is the external ref for Acme",
            ),
        ],
    )
    assert package.attribution_texts == [
        "The GNU C Library is free software.  See the file COPYING.LIB for copying conditions, and LICENSES for "
        "notices about a few contributions that require these additional notices to be distributed.  License "
        "copyright years may be listed using range notation, e.g., 1996-2015, indicating that every year in the "
        "range, inclusive, is a copyrightable year that would otherwise be listed individually."
    ]
    assert package.primary_package_purpose == PackagePurpose.SOURCE
    assert package.release_date == datetime(2012, 1, 29, 18, 30, 22)
    assert package.built_date == datetime(2011, 1, 29, 18, 30, 22)
    assert package.valid_until_date == datetime(2014, 1, 29, 18, 30, 22)


@pytest.mark.parametrize(
    "incomplete_package_dict",
    [
        {"SPDXID": "SPDXRef-Package"},
        {"SPDXID": "SPDXRef-Package", "name": 5, "downloadLocation": "NONE"},
        {
            "SPDXID": "SPDXRef-Package",
            "name": "Example Package",
            "downloadLocation": "NONE",
            "checksums": [{"algorithm": "SHA", "value": "1234"}],
        },
    ],
)
def test_parse_invalid_package(incomplete_package_dict):
    package_parser = PackageParser()

    with pytest.raises(SPDXParsingError):
        package_parser.parse_package(incomplete_package_dict)


def test_parse_packages():
    package_parser = PackageParser()
    packages_list = [
        {
            "SPDXID": "SPDXRef-Package",
            "name": "Example Package",
            "downloadLocation": "NONE",
            "checksums": [{"algorithm": "SHA", "value": "1234"}],
        },
        {"SPDXID": "SPDXRef-Package", "name": 5, "downloadLocation": "NONE"},
        {"SPDXID": "SPDXRef-Package", "name": "Example Package", "downloadLocation": "NONE"},
    ]

    with pytest.raises(SPDXParsingError):
        parse_list_of_elements(packages_list, package_parser.parse_package)


def test_parse_external_ref():
    package_parser = PackageParser()
    external_ref = {"referenceType": "fix"}

    with pytest.raises(SPDXParsingError):
        package_parser.parse_external_ref(external_ref)


def test_parse_invalid_external_package_ref_category():
    package_parser = PackageParser()
    external_package_ref_category = "TEST"

    with pytest.raises(SPDXParsingError) as err:
        package_parser.parse_external_ref_category(external_package_ref_category)

    TestCase().assertCountEqual(err.value.get_messages(), ["Invalid ExternalPackageRefCategory: TEST"])
