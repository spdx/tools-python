
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

from datetime import datetime
import unittest
from unittest import TestCase

import spdx.config as config
from spdx.creationinfo import CreationInfo
from spdx.creationinfo import Tool
from spdx.creationinfo import Organization
from spdx.creationinfo import Person
from spdx.version import Version


class TestCreationInfo(TestCase):

    def test_timestamp(self):
        dt = datetime(2014, 4, 8, 13, 42, 12)
        ci_time = CreationInfo(created=dt)
        assert ci_time.created == dt

    def test_iso_format(self):
        dt = datetime(2014, 4, 8, 13, 42, 12)
        ci_time = CreationInfo(created=dt)
        assert ci_time.created_iso_format == "2014-04-08T13:42:12Z"

    def test_comment(self):
        ci_default = CreationInfo()
        assert ci_default.comment is None
        ci_comment = CreationInfo(comment='Hello There')
        assert ci_comment.comment == 'Hello There'

    def test_creators(self):
        ci = CreationInfo()
        assert len(ci.creators) == 0
        person = Person(name='Alice', email='alice@example.com')
        tool = Tool(name='spdxtron-9000')
        org = Organization(name='Acme', email='acme@example.com')
        ci.add_creator(tool)
        ci.add_creator(org)
        ci.add_creator(person)
        assert len(ci.creators) == 3
        assert tool in ci.creators
        assert org in ci.creators
        assert person in ci.creators
        ci.remove_creator(person)
        assert len(ci.creators) == 2
        assert tool in ci.creators
        assert org in ci.creators
        assert person not in ci.creators

    def test_license_list_version(self):
        ci = CreationInfo()
        assert ci.license_list_version == config.LICENSE_LIST_VERSION
        ci = CreationInfo(license_list_version=Version(major=1, minor=0))
        assert ci.license_list_version == Version(major=1, minor=0)
        assert not ci.license_list_version == Version(major=1, minor=2)


if __name__ == '__main__':
    unittest.main()