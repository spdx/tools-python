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

import unittest
from unittest import TestCase

from spdx.version import Version
from spdx.document import Document
from spdx.document import License
from spdx.config import LICENSE_MAP


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