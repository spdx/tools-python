
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

from collections import OrderedDict
import io
import json
from unittest import TestCase

from spdx.parsers import jsonparser, yamlparser, xmlparser
from spdx.parsers.jsonyamlxmlbuilders import Builder
from spdx.parsers.loggers import StandardLogger

from tests import utils_test
from tests.utils_test import TestParserUtils


class TestParser(TestCase):
    maxDiff = None

    def check_document(self, document, expected_loc, regen=False):
        result = TestParserUtils.to_dict(document)

        if regen:
            with open(expected_loc, 'w') as o:
                o.write(json.dumps(result, indent=2))

        with io.open(expected_loc, encoding='utf-8') as ex:
            expected = json.load(ex, object_pairs_hook=OrderedDict)

        assert result == expected

    def test_json_parser(self):
        parser = jsonparser.Parser(Builder(), StandardLogger())
        test_file = utils_test.get_test_loc('formats/SPDXJsonExample.json')
        with io.open(test_file, encoding='utf-8') as f:
            document, _ = parser.parse(f)
        expected_loc = utils_test.get_test_loc('doc_parse/expected.json')
        self.check_document(document, expected_loc)

    def test_yaml_parser(self):
        parser = yamlparser.Parser(Builder(), StandardLogger())
        test_file = utils_test.get_test_loc('formats/SPDXYamlExample.yaml')
        with io.open(test_file, encoding='utf-8') as f:
            document, _ = parser.parse(f)
        expected_loc = utils_test.get_test_loc('doc_parse/expected.json')
        self.check_document(document, expected_loc)

    def test_xml_parser(self):
        parser = xmlparser.Parser(Builder(), StandardLogger())
        test_file = utils_test.get_test_loc('formats/SPDXXmlExample.xml')
        with io.open(test_file, encoding='utf-8') as f:
            document, _ = parser.parse(f)
        expected_loc = utils_test.get_test_loc('doc_parse/expected.json')
        self.check_document(document, expected_loc)

    def test_sbomyaml_parser(self):
        parser = yamlparser.Parser(Builder(), StandardLogger())
        test_file = utils_test.get_test_loc('formats/SPDXSBOMExample.spdx.yml')
        with io.open(test_file, encoding='utf-8') as f:
            document, errors = parser.parse(f)
            assert not errors
        expected_loc = utils_test.get_test_loc('doc_parse/SBOMexpected.json')
        self.check_document(document, expected_loc)
