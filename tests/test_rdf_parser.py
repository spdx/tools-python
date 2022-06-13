
# Copyright (c) the SPDX tools authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import json
import unittest

from spdx.parsers import rdf
from spdx.parsers.loggers import StandardLogger
from spdx.parsers.rdfbuilders import Builder as RDFBuilder

from tests import utils_test
from tests.utils_test import TestParserUtils


class TestParser(unittest.TestCase):
    maxDiff = None

    def test_rdf_parser(self, regen=False):
        parser = rdf.Parser(RDFBuilder(), StandardLogger())
        test_file = utils_test.get_test_loc('formats/SPDXRdfExample.rdf', test_data_dir=utils_test.test_data_dir)
        with io.open(test_file, 'rb') as f:
            document, _ = parser.parse(f)
        expected_loc = utils_test.get_test_loc('doc_parse/spdx-expected.json', test_data_dir=utils_test.test_data_dir)
        self.check_document(document, expected_loc, regen=regen)

    def check_document(self, document, expected_loc, regen=False):
        result = TestParserUtils.to_dict(document)

        if regen:
            data = json.dumps(result, indent=2)
            with io.open(expected_loc, 'w') as o:
                o.write(data)

        with io.open(expected_loc, 'r', encoding='utf-8') as ex:
            expected = json.load(ex)

        assert result == expected

    def test_rdf_parser_unpacked_files(self, regen=False):
        parser = rdf.Parser(RDFBuilder(), StandardLogger())
        test_file = utils_test.get_test_loc('formats/SPDXRdfUnpackagedFileExample.rdf', test_data_dir=utils_test.test_data_dir)
        with io.open(test_file, 'rb') as f:
            document, _ = parser.parse(f)
        expected_loc = utils_test.get_test_loc('doc_parse/spdx-expected-unpackaged-files.json', test_data_dir=utils_test.test_data_dir)
        self.check_document(document, expected_loc, regen=regen)

