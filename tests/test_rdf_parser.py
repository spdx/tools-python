
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

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import io
import json
import unittest

import six

from spdx.parsers import rdf
from spdx.parsers.loggers import StandardLogger
from spdx.parsers.rdfbuilders import Builder as RDFBuilder

from tests import utils_test
from tests.utils_test import TestParserUtils


class TestParser(unittest.TestCase):
    maxDiff = None

    def test_rdf_parser(self):
        parser = rdf.Parser(RDFBuilder(), StandardLogger())
        test_file = utils_test.get_test_loc('formats/SPDXRdfExample.rdf', test_data_dir=utils_test.test_data_dir)
        with io.open(test_file, 'rb') as f:
            document, _ = parser.parse(f)
        expected_loc = utils_test.get_test_loc('doc_parse/spdx-expected.json', test_data_dir=utils_test.test_data_dir)
        self.check_document(document, expected_loc)

    def check_document(self, document, expected_loc, regen=False):
        result = TestParserUtils.to_dict(document)

        if regen:
            data = json.dumps(result, indent=2)
            if six.PY3:
                data = data.encode('utf-8')
            with io.open(expected_loc, 'wb') as o:
                o.write(data)

        with io.open(expected_loc, 'r', encoding='utf-8') as ex:
            expected = json.load(ex)

        self.check_fields(result, expected)
        assert expected == result

    def check_fields(self, result, expected):
        """
        Test result and expected objects field by field
        to provide more specific error messages when failing
        """
        assert expected['id'] == result['id']
        assert expected['specVersion'] == result['specVersion']
        assert expected['documentNamespace'] == result['documentNamespace']
        assert expected['name'] == result['name']
        assert expected['comment'] == result['comment']
        assert expected['dataLicense'] == result['dataLicense']
        assert expected['licenseListVersion'] == result['licenseListVersion']
        assert expected['creators'] == result['creators']
        assert expected['created'] == result['created']
        assert expected['creatorComment'] == result['creatorComment']
        assert expected['package']['files'] == result['package']['files']
        assert expected['package'] == result['package']
        assert expected['externalDocumentRefs'] == result['externalDocumentRefs']
        assert expected['extractedLicenses'] == result['extractedLicenses']
        assert expected['annotations'] == result['annotations']
        assert expected['reviews'] == result['reviews']
