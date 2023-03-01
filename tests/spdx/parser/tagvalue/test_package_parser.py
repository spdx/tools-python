# Copyright (c) 2023 spdx contributors
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
from unittest import TestCase

from license_expression import get_spdx_licensing

from spdx.model.package import ExternalPackageRef, ExternalPackageRefCategory, PackagePurpose
from spdx.parser.tagvalue.parser.tagvalue import Parser
from tests.spdx.parser.tagvalue.test_creation_info_parser import DOCUMENT_STR


def test_package():
    parser = Parser()
    package_str = '\n'.join([
        'PackageName: Test',
        'SPDXID: SPDXRef-Package',
        'PackageVersion: Version 0.9.2',
        'PackageDownloadLocation: http://example.com/test',
        'FilesAnalyzed: True',
        'PackageSummary: <text>Test package</text>',
        'PackageSourceInfo: <text>Version 1.0 of test</text>',
        'PackageFileName: test-1.0.zip',
        'PackageSupplier: Organization:ACME',
        'PackageOriginator: Organization:ACME',
        'PackageChecksum: SHA1: 2fd4e1c67a2d28fced849ee1bb76e7391b93eb12',
        'PackageVerificationCode: 4e3211c67a2d28fced849ee1bb76e7391b93feba (something.rdf, something.txt)',
        'PackageDescription: <text>A package.</text>',
        'PackageComment: <text>Comment on the package.</text>',
        'PackageCopyrightText: <text> Copyright 2014 Acme Inc.</text>',
        'PackageLicenseDeclared: Apache-2.0',
        'PackageLicenseConcluded: (LicenseRef-2.0 and Apache-2.0)',
        'PackageLicenseInfoFromFiles: Apache-1.0',
        'PackageLicenseInfoFromFiles: Apache-2.0',
        'PackageLicenseComments: <text>License Comments</text>',
        'ExternalRef: SECURITY cpe23Type cpe:2.3:a:pivotal_software:spring_framework:4.1.0:*:*:*:*:*:*:',
        'ExternalRefComment: <text>Some comment about the package.</text>',
        'ExternalRef: OTHER LocationRef-acmeforge acmecorp/acmenator/4.1.3-alpha',
        'PrimaryPackagePurpose: OPERATING-SYSTEM',
        'BuiltDate: 2020-01-01T12:00:00Z',
        'ReleaseDate: 2021-01-01T12:00:00Z',
        'ValidUntilDate: 2022-01-01T12:00:00Z'
    ])
    document = parser.parse("\n".join([DOCUMENT_STR, package_str]))
    assert document is not None
    package = document.packages[0]
    assert package.name == 'Test'
    assert package.spdx_id == 'SPDXRef-Package'
    assert package.version == 'Version 0.9.2'
    assert len(package.license_info_from_files) == 2
    assert package.license_concluded == get_spdx_licensing().parse('LicenseRef-2.0 AND Apache-2.0')
    assert package.files_analyzed is True
    assert package.comment == 'Comment on the package.'
    assert len(package.external_references) == 2
    TestCase().assertCountEqual(package.external_references,
                                [ExternalPackageRef(ExternalPackageRefCategory.SECURITY, "cpe23Type",
                                                    "cpe:2.3:a:pivotal_software:spring_framework:4.1.0:*:*:*:*:*:*:",
                                                    "Some comment about the package."),
                                 ExternalPackageRef(ExternalPackageRefCategory.OTHER, "LocationRef-acmeforge",
                                                    "acmecorp/acmenator/4.1.3-alpha")])
    assert package.primary_package_purpose == PackagePurpose.OPERATING_SYSTEM
    assert package.built_date == datetime(2020, 1, 1, 12, 0, 0)
    assert package.release_date == datetime(2021, 1, 1, 12, 0, 0)
    assert package.valid_until_date == datetime(2022, 1, 1, 12, 0, 0)