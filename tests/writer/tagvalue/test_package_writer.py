#  Copyright (c) 2022 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from datetime import datetime
from unittest.mock import patch, mock_open, call

from src.model.license_expression import LicenseExpression
from src.model.package import PackagePurpose
from src.model.spdx_no_assertion import SpdxNoAssertion
from src.model.spdx_none import SpdxNone
from src.writer.tagvalue.package_writer import write_package
from tests.valid_defaults import get_package, get_package_verification_code, get_actor, get_checksum, \
    get_external_package_ref


def test_package_writer():
    package = get_package("SPDXRef-Package", "package name", "www.download.com", "version", "file_name", SpdxNoAssertion(),
                      get_actor(), True,
                      get_package_verification_code(), [get_checksum()], "https://homepage.com", "source_info", None,
                      [LicenseExpression("expression")],
                      SpdxNone(), "comment on license", "copyright", "summary", "description", "comment",
                      [get_external_package_ref()], ["text"], PackagePurpose.OTHER, datetime(2022, 1, 1), None, None)

    m = mock_open()
    with patch('{}.open'.format(__name__), m, create=True):
        with open('foo', 'w') as h:
            write_package(package, h)

    m.assert_called_once_with('foo', 'w')
    handle = m()
    handle.write.assert_has_calls(
        [call('## Package Information\n'), call('PackageName: package name\n'), call('SPDXID: SPDXRef-Package\n'),
         call('PackageVersion: version\n'), call('PackageDownloadLocation: www.download.com\n'),
         call('FilesAnalyzed: True\n'), call('PackageSummary: summary\n'), call('PackageAttributionText: text\n'),
         call('PackageSourceInfo: source_info\n'), call('PackageFileName: file_name\n'),
         call('PackageSupplier: NOASSERTION\n'),
         call("PackageOriginator: Person: person name\n"),
         call('PackageChecksum: SHA1: 85ed0817af83a24ad8da68c2b5094de69833983c\n'),
         call('PackageVerificationCode: 85ed0817af83a24ad8da68c2b5094de69833983c\n'),
         call('PackageDescription: description\n'), call('PackageComment: comment\n'),
         call('PackageLicenseDeclared: NONE\n'),
         call("PackageLicenseInfoFromFiles: expression\n"),
         call('PackageLicenseComments: comment on license\n'), call('PackageCopyrightText: copyright\n'),
         call('PackageHomePage: https://homepage.com\n'),
         call('ExternalRef: SECURITY cpe22Type cpe:/o:canonical:ubuntu_linux:10.04:-:lts\n'),
         call('ExternalRefComment: external package ref comment\n'), call('PrimaryPackagePurpose: OTHER\n'),
         call('ReleaseDate: 2022-01-01T00:00:00Z\n')])
