# Copyright (c) 2022 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from datetime import datetime

from src.model.actor import Actor, ActorType
from src.model.checksum import Checksum, ChecksumAlgorithm
from src.model.license_expression import LicenseExpression
from src.model.package import PackageVerificationCode, ExternalPackageRef, ExternalPackageRefCategory, PackagePurpose
from src.parser.json.package_parser import PackageParser


def test_package_parser():
    package_parser = PackageParser()

    package_dict = {
        "SPDXID": "SPDXRef-Package",
        "attributionTexts": [
            "The GNU C Library is free software.  See the file COPYING.LIB for copying conditions, and LICENSES for notices about a few contributions that require these additional notices to be distributed.  License copyright years may be listed using range notation, e.g., 1996-2015, indicating that every year in the range, inclusive, is a copyrightable year that would otherwise be listed individually."],
        "builtDate": "2011-01-29T18:30:22Z",
        "checksums": [{
            "algorithm": "MD5",
            "checksumValue": "624c1abb3664f4b35547e7c73864ad24"
        }, {
            "algorithm": "SHA1",
            "checksumValue": "85ed0817af83a24ad8da68c2b5094de69833983c"
        }, {
            "algorithm": "SHA256",
            "checksumValue": "11b6d3ee554eedf79299905a98f9b9a04e498210b59f15094c916c91d150efcd"
        }, {
            "algorithm": "BLAKE2b-384",
            "checksumValue": "aaabd89c926ab525c242e6621f2f5fa73aa4afe3d9e24aed727faaadd6af38b620bdb623dd2b4788b1c8086984af8706"
        }],
        "comment": "This is a comment.",
        "copyrightText": "Copyright 2008-2010 John Smith",
        "description": "The GNU C Library defines functions that are specified by the ISO C standard, as well as additional features specific to POSIX and other derivatives of the Unix operating system, and extensions specific to GNU systems.",
        "downloadLocation": "http://ftp.gnu.org/gnu/glibc/glibc-ports-2.15.tar.gz",
        "externalRefs": [{
            "referenceCategory": "SECURITY",
            "referenceLocator": "cpe:2.3:a:pivotal_software:spring_framework:4.1.0:*:*:*:*:*:*:*",
            "referenceType": "cpe23Type"
        }, {
            "comment": "This is the external ref for Acme",
            "referenceCategory": "OTHER",
            "referenceLocator": "acmecorp/acmenator/4.1.3-alpha",
            "referenceType": "http://spdx.org/spdxdocs/spdx-example-444504E0-4F89-41D3-9A0C-0305E82C3301#LocationRef-acmeforge"
        }],
        "filesAnalyzed": True,
        "homepage": "http://ftp.gnu.org/gnu/glibc",
        "licenseComments": "The license for this project changed with the release of version x.y.  The version of the project included here post-dates the license change.",
        "licenseConcluded": "(LGPL-2.0-only OR LicenseRef-3)",
        "licenseDeclared": "(LGPL-2.0-only AND LicenseRef-3)",
        "licenseInfoFromFiles": ["GPL-2.0-only", "LicenseRef-2", "LicenseRef-1"],
        "name": "glibc",
        "originator": "Organization: ExampleCodeInspect (contact@example.com)",
        "packageFileName": "glibc-2.11.1.tar.gz",
        "packageVerificationCode": {
            "packageVerificationCodeExcludedFiles": ["./package.spdx"],
            "packageVerificationCodeValue": "d6a770ba38583ed4bb4525bd96e50461655d2758"
        },
        "primaryPackagePurpose": "SOURCE",
        "releaseDate": "2012-01-29T18:30:22Z",
        "sourceInfo": "uses glibc-2_11-branch from git://sourceware.org/git/glibc.git.",
        "summary": "GNU C library.",
        "supplier": "Person: Jane Doe (jane.doe@example.com)",
        "validUntilDate": "2014-01-29T18:30:22Z",
        "versionInfo": "2.11.1"
    }

    package = package_parser.parse_package(package_dict)

    assert package.spdx_id == "SPDXRef-Package"
    assert package.name == "glibc"
    assert package.download_location == "http://ftp.gnu.org/gnu/glibc/glibc-ports-2.15.tar.gz"
    assert package.version == "2.11.1"
    assert package.file_name == "glibc-2.11.1.tar.gz"
    assert package.supplier == Actor(ActorType.PERSON, "Jane Doe", "jane.doe@example.com")
    assert package.originator == Actor(ActorType.ORGANIZATION, "ExampleCodeInspect", "contact@example.com")
    assert package.files_analyzed == True
    assert package.verification_code == PackageVerificationCode(value="d6a770ba38583ed4bb4525bd96e50461655d2758",
                                                                excluded_files=["./package.spdx"])
    assert len(package.checksums) == 4
    assert package.checksums == [Checksum(ChecksumAlgorithm.MD5, "624c1abb3664f4b35547e7c73864ad24"),
                                 Checksum(ChecksumAlgorithm.SHA1, "85ed0817af83a24ad8da68c2b5094de69833983c"),
                                 Checksum(ChecksumAlgorithm.SHA256,
                                          "11b6d3ee554eedf79299905a98f9b9a04e498210b59f15094c916c91d150efcd"),
                                 Checksum(ChecksumAlgorithm.BLAKE2B_384,
                                          "aaabd89c926ab525c242e6621f2f5fa73aa4afe3d9e24aed727faaadd6af38b620bdb623dd2b4788b1c8086984af8706")]
    assert package.homepage == "http://ftp.gnu.org/gnu/glibc"
    assert package.source_info == "uses glibc-2_11-branch from git://sourceware.org/git/glibc.git."
    assert package.license_concluded == LicenseExpression("(LGPL-2.0-only OR LicenseRef-3)")
    assert package.license_info_from_files == [LicenseExpression("GPL-2.0-only"), LicenseExpression("LicenseRef-2"),
                                               LicenseExpression("LicenseRef-1")]
    assert package.license_declared == LicenseExpression("(LGPL-2.0-only AND LicenseRef-3)")
    assert package.license_comment == "The license for this project changed with the release of version x.y.  The version of the project included here post-dates the license change."
    assert package.copyright_text == "Copyright 2008-2010 John Smith"
    assert package.summary == "GNU C library."
    assert package.description == "The GNU C Library defines functions that are specified by the ISO C standard, as well as additional features specific to POSIX and other derivatives of the Unix operating system, and extensions specific to GNU systems."
    assert package.comment == "This is a comment."
    assert len(package.external_references) == 2
    assert package.external_references == [ExternalPackageRef(ExternalPackageRefCategory.SECURITY, "cpe23Type",
                                                              "cpe:2.3:a:pivotal_software:spring_framework:4.1.0:*:*:*:*:*:*:*"),
                                           ExternalPackageRef(ExternalPackageRefCategory.OTHER,
                                                              "http://spdx.org/spdxdocs/spdx-example-444504E0-4F89-41D3-9A0C-0305E82C3301#LocationRef-acmeforge",
                                                              locator="acmecorp/acmenator/4.1.3-alpha",
                                                              comment="This is the external ref for Acme")]
    assert package.attribution_texts == [
        "The GNU C Library is free software.  See the file COPYING.LIB for copying conditions, and LICENSES for notices about a few contributions that require these additional notices to be distributed.  License copyright years may be listed using range notation, e.g., 1996-2015, indicating that every year in the range, inclusive, is a copyrightable year that would otherwise be listed individually."]
    assert package.primary_package_purpose == PackagePurpose.SOURCE
    assert package.release_date == datetime(2012, 1, 29, 18, 30, 22)
    assert package.built_date == datetime(2011, 1, 29, 18, 30, 22)
    assert package.valid_until_date == datetime(2014, 1, 29, 18, 30, 22)
