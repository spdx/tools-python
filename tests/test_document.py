# Copyright (c) 2014 Ahmed H. Ismail
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import shutil
import tempfile
import unittest
from unittest import TestCase

from spdx.checksum import Algorithm
from spdx.config import LICENSE_MAP
from spdx.creationinfo import Tool
from spdx.document import Document
from spdx.document import License
from spdx.file import File
from spdx.package import Package
from spdx.utils import NoAssert
from spdx.version import Version

from tests import utils_test


class TestVersion(TestCase):

    def test_creation(self):
        v = Version(major=1, minor=2)
        assert v.major == 1
        assert v.minor == 2

    def test_comparison(self):
        v1 = Version(major=1, minor=2)
        v2 = Version(major=2, minor=1)
        assert v1 != v2
        assert v1 < v2
        assert v1 <= v2
        assert v2 > v1
        assert v2 >= v1
        v3 = Version(major=1, minor=2)
        assert v3 == v1
        assert not v1 < v3
        assert v1 <= v3


class TestDocument(TestCase):

    def test_creation(self):
        document = Document(
            version=Version(major=1, minor=2),
            data_license=License(full_name='Academic Free License v1.1',
                                identifier='AFL-1.1')
        )
        assert document.comment is None
        assert document.version == Version(1, 2)
        assert document.data_license.identifier == 'AFL-1.1'

    def test_document_validate_failures_returns_informative_messages(self):
        doc = Document(Version(2, 1), License.from_identifier('CC0-1.0'))
        pack = doc.package = Package('some/path', NoAssert())
        file1 = File('./some/path/tofile')
        file1.name = './some/path/tofile'
        file1.chk_sum = Algorithm('SHA1', 'SOME-SHA1')
        lic1 = License.from_identifier('LGPL-2.1')
        file1.add_lics(lic1)
        pack.add_lics_from_file(lic1)
        messages = []
        is_valid = doc.validate(messages)
        assert not is_valid
        expected = [
            'No creators defined, must have at least one.'
        ]
        assert expected == messages

    def test_document_is_valid_when_using_or_later_licenses(self):
        doc = Document(Version(2, 1), License.from_identifier('CC0-1.0'))
        doc.creation_info.add_creator(Tool('ScanCode'))
        doc.creation_info.set_created_now()

        package = doc.package = Package(name='some/path', download_location=NoAssert())
        package.cr_text = 'Some copyrught'
        package.verif_code = 'SOME code'
        package.license_declared = NoAssert()
        package.conc_lics = NoAssert()

        file1 = File('./some/path/tofile')
        file1.name = './some/path/tofile'
        file1.chk_sum = Algorithm('SHA1', 'SOME-SHA1')
        file1.conc_lics = NoAssert()
        file1.copyright = NoAssert()

        lic1 = License.from_identifier('LGPL-2.1+')
        file1.add_lics(lic1)

        package.add_lics_from_file(lic1)
        package.add_file(file1)
        messages = []
        is_valid = doc.validate(messages)
        assert is_valid
        assert not messages


class TestWriters(TestCase):

    def _get_lgpl_doc(self, or_later=False):
        doc = Document(Version(2, 1), License.from_identifier('CC0-1.0'))
        doc.creation_info.add_creator(Tool('ScanCode'))
        doc.creation_info.set_created_now()

        package = doc.package = Package(name='some/path', download_location=NoAssert())
        package.cr_text = 'Some copyrught'
        package.verif_code = 'SOME code'
        package.license_declared = NoAssert()
        package.conc_lics = NoAssert()

        file1 = File('./some/path/tofile')
        file1.name = './some/path/tofile'
        file1.chk_sum = Algorithm('SHA1', 'SOME-SHA1')
        file1.conc_lics = NoAssert()
        file1.copyright = NoAssert()

        lic1 = License.from_identifier('LGPL-2.1')
        if or_later:
            lic1 = License.from_identifier('LGPL-2.1+')

        file1.add_lics(lic1)

        package.add_lics_from_file(lic1)
        package.add_file(file1)
        return doc

    def test_write_document_rdf_with_validate(self):
        from spdx.writers.rdf import write_document
        doc = self._get_lgpl_doc()
        temp_dir = ''
        try:
            temp_dir = tempfile.mkdtemp(prefix='test_spdx')
            result_file = os.path.join(temp_dir, 'spdx-simple.rdf')
            with open(result_file, 'wb') as output:
                write_document(doc, output, validate=True)

            expected_file = utils_test.get_test_loc(
                'doc_write/rdf-simple.json',
                test_data_dir=utils_test.test_data_dir)

            utils_test.check_rdf_scan(expected_file, result_file, regen=False)
        finally:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

    def test_write_document_rdf_with_or_later_with_validate(self):
        from spdx.writers.rdf import write_document
        doc = self._get_lgpl_doc(or_later=True)

        temp_dir = ''
        try:
            temp_dir = tempfile.mkdtemp(prefix='test_spdx')
            result_file = os.path.join(temp_dir, 'spdx-simple-plus.rdf')

            # test proper!
            with open(result_file, 'wb') as output:
                write_document(doc, output, validate=True)

            expected_file = utils_test.get_test_loc(
                'doc_write/rdf-simple-plus.json',
                test_data_dir=utils_test.test_data_dir)

            utils_test.check_rdf_scan(expected_file, result_file, regen=False)
        finally:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

    def test_write_document_tv_with_validate(self):
        from spdx.writers.tagvalue import write_document
        doc = self._get_lgpl_doc()

        temp_dir = ''
        try:
            temp_dir = tempfile.mkdtemp(prefix='test_spdx')
            result_file = os.path.join(temp_dir, 'spdx-simple.tv')
            with open(result_file, 'wb') as output:
                write_document(doc, output, validate=True)

            expected_file = utils_test.get_test_loc(
                'doc_write/tv-simple.tv',
                test_data_dir=utils_test.test_data_dir)

            utils_test.check_tv_scan(expected_file, result_file, regen=False)
        finally:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

    def test_write_document_tv_with_or_later_with_validate(self):
        from spdx.writers.tagvalue import write_document

        doc = self._get_lgpl_doc(or_later=True)

        temp_dir = ''
        try:
            temp_dir = tempfile.mkdtemp(prefix='test_spdx')
            result_file = os.path.join(temp_dir, 'spdx-simple-plus.tv')

            # test proper!
            with open(result_file, 'wb') as output:
                write_document(doc, output, validate=True)

            expected_file = utils_test.get_test_loc(
                'doc_write/tv-simple-plus.tv',
                test_data_dir=utils_test.test_data_dir)

            utils_test.check_tv_scan(expected_file, result_file, regen=False)
        finally:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)


class TestLicense(TestCase):

    def test_url(self):
        lic = License(full_name='Apache License 1.0', identifier='Apache-1.0')
        assert lic.url == 'http://spdx.org/licenses/Apache-1.0'

    def test_license_list(self):
        assert LICENSE_MAP['Aladdin Free Public License'] == 'Aladdin'
        assert LICENSE_MAP['Aladdin'] == 'Aladdin Free Public License'
        assert LICENSE_MAP['MIT License'] == 'MIT'
        assert LICENSE_MAP['MIT'] == 'MIT License'
        assert LICENSE_MAP['BSD 4-clause "Original" or "Old" License'] == 'BSD-4-Clause'
        assert LICENSE_MAP['BSD-4-Clause'] == 'BSD 4-clause "Original" or "Old" License'

    def test_from_full_name(self):
        mit = License.from_full_name('MIT License')
        assert mit.identifier == 'MIT'
        assert mit.url == 'http://spdx.org/licenses/MIT'

    def test_from_identifier(self):
        mit = License.from_identifier('MIT')
        assert mit.full_name == 'MIT License'
        assert mit.url == 'http://spdx.org/licenses/MIT'


if __name__ == '__main__':
    unittest.main()