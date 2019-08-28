
# Copyright (c) Xavier Figueroa
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

import io
import json
import sys
from unittest import TestCase

from spdx.parsers import jsonparser, yamlparser, xmlparser
from spdx.parsers.jsonyamlxmlbuilders import Builder
from spdx.parsers.loggers import StandardLogger

from tests import utils_test
from tests.utils_test import TestParserUtils


_sys_v0 = sys.version_info[0]
py2 = _sys_v0 == 2
py3 = _sys_v0 == 3


class TestParser(TestCase):
    maxDiff = None

    def test_json_parser(self):
        parser = jsonparser.Parser(Builder(), StandardLogger())
        test_file = utils_test.get_test_loc('formats/SPDXJsonExample.json', test_data_dir=utils_test.test_data_dir)
        with open(test_file, 'r') as f:
            document, _ = parser.parse(f)
        expected_loc = utils_test.get_test_loc('doc_parse/expected.json', test_data_dir=utils_test.test_data_dir)
        self.check_document(document, expected_loc)

    def test_yaml_parser(self):
        parser = yamlparser.Parser(Builder(), StandardLogger())
        test_file = utils_test.get_test_loc('formats/SPDXYamlExample.yaml', test_data_dir=utils_test.test_data_dir)
        with open(test_file, 'r') as f:
            document, _ = parser.parse(f)
        expected_loc = utils_test.get_test_loc('doc_parse/expected.json', test_data_dir=utils_test.test_data_dir)
        self.check_document(document, expected_loc)

    def test_xml_parser(self):
        parser = xmlparser.Parser(Builder(), StandardLogger())
        test_file = utils_test.get_test_loc('formats/SPDXXmlExample.xml', test_data_dir=utils_test.test_data_dir)
        with open(test_file, 'r') as f:
            document, _ = parser.parse(f)
        expected_loc = utils_test.get_test_loc('doc_parse/expected.json', test_data_dir=utils_test.test_data_dir)
        self.check_document(document, expected_loc)

    def check_document(self, document, expected_loc, regen=False):
        result = TestParserUtils.to_dict(document)

        if regen:
            with open(expected_loc, 'wb') as o:
                o.write(json.dumps(result, indent=2))

        with io.open(expected_loc, encoding='utf-8') as ex:
            expected = json.load(ex, encoding='utf-8',)

        self.assertEqual(expected, result)
