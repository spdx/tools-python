from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import unittest
import json
from unittest import TestCase
from tests import utils_test
from tests.utils_test import TestParserUtils
from spdx.parsers import rdf
from spdx.parsers.rdfbuilders import Builder as RDFBuilder
from spdx.parsers.loggers import StandardLogger


class TestParser(TestCase):

    def test_rdf_parser(self):
        parser = rdf.Parser(RDFBuilder(), StandardLogger())
        test_file = utils_test.get_test_loc('../../data/SPDXRdfExample.rdf', test_data_dir=utils_test.test_data_dir)
        with open(test_file, 'r') as file:
            document, _ = parser.parse(file)
        expected_loc = utils_test.get_test_loc('doc_parse/spdx-expected.json', test_data_dir=utils_test.test_data_dir)
        self.check_document(document, expected_loc)
    
    def check_document(self, document, expected_loc, regen=False):
        result = TestParserUtils.to_dict(document)

        if regen:
            with open(expected_loc, 'w', encoding='utf-8') as o:
                o.write(result)

        with open(expected_loc, 'r') as ex:
            expected = json.load(ex, encoding='utf-8')

        self.check_fields(result, expected)
        assert result == expected
        
    def check_fields(self, result, expected):
        """
        Test result and expected objects field by field 
        to provide more specific error messages when failing
        """
        assert result['id'] == expected['id']
        assert result['specVersion'] == expected['specVersion']
        assert result['namespace'] == expected['namespace']
        assert result['name'] == expected['name']
        assert result['comment'] == expected['comment']
        assert result['dataLicense'] == expected['dataLicense']
        assert result['licenseListVersion'] == expected['licenseListVersion']
        assert result['creators'] == expected['creators']
        assert result['created'] == expected['created']
        assert result['creatorComment'] == expected['creatorComment']
        assert result['package']['files'] == expected['package']['files']
        assert result['package'] == expected['package']
        assert result['externalDocumentRefs'] == expected['externalDocumentRefs']
        assert result['extractedLicenses'] == expected['extractedLicenses']
        assert result['annotations'] == expected['annotations']
        assert result['reviews'] == expected['reviews']
        

if __name__ == '__main__':
    unittest.main()
