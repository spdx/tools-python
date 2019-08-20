from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import io
import json
import unittest

import six

from tests import utils_test
from tests.utils_test import TestParserUtils

from spdx.parsers import rdf
from spdx.parsers.rdf import Parser
from spdx.parsers.rdfbuilders import Builder
from spdx.parsers.rdfbuilders import Builder as RDFBuilder
from spdx.parsers.loggers import StandardLogger


class TestParser(unittest.TestCase):

    def test_rdf_parser(self):
        parser = rdf.Parser(RDFBuilder(), StandardLogger())
        test_file = utils_test.get_test_loc('../../data/SPDXRdfExample.rdf', test_data_dir=utils_test.test_data_dir)
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

    @unittest.expectedFailure
    def test_extracted_licenses(self):
        parser = Parser(Builder(), StandardLogger())
        test_file = utils_test.get_test_loc('../../data/SPDXRdfExample.rdf', test_data_dir=utils_test.test_data_dir)
        with open(test_file, 'r') as f:
            document, _ = parser.parse(f)
        assert len(document.extracted_licenses) == 4
        # It is needed to sort the list because the order changes when parsing
        licenses = sorted(document.extracted_licenses)
        assert licenses[0].identifier.toPython() == 'LicenseRef-1'
        assert licenses[1].identifier.toPython() == 'LicenseRef-2'
        assert licenses[2].identifier.toPython() == 'LicenseRef-3'
        assert licenses[3].identifier.toPython() == 'LicenseRef-4'

    def test_pkg_lic_decl(self):
        parser = Parser(Builder(), StandardLogger())
        test_file = utils_test.get_test_loc('../../data/SPDXRdfExample.rdf', test_data_dir=utils_test.test_data_dir)
        with open(test_file, 'r') as f:
            document, _ = parser.parse(f)
        # It is needed to ckeck it as sorted lists because the order changes when parsing
        lic_expected = ['Apache-2.0', 'LicenseRef-1', 'LicenseRef-2', 'LicenseRef-3', 'LicenseRef-4', 'MPL-1.1']
        lic_result = sorted(document.package.license_declared.identifier.split(' AND '))
        assert lic_result == lic_expected

    def test_pkg_lic_conc(self):
        parser = Parser(Builder(), StandardLogger())
        test_file = utils_test.get_test_loc('../../data/SPDXRdfExample.rdf', test_data_dir=utils_test.test_data_dir)
        with open(test_file, 'r') as f:
            document, _ = parser.parse(f)
        # It is needed to ckeck it as sorted lists because the order changes when parsing
        lic_expected = ['Apache-1.0', 'Apache-2.0', 'LicenseRef-1', 'LicenseRef-2', 'LicenseRef-3', 'LicenseRef-4', 'MPL-1.1']
        lic_result = sorted(document.package.conc_lics.identifier.split(' AND '))
        assert lic_result == lic_expected

    @unittest.expectedFailure
    def test_file_lic_conc(self):
        parser = Parser(Builder(), StandardLogger())
        test_file = utils_test.get_test_loc('../../data/SPDXRdfExample.rdf', test_data_dir=utils_test.test_data_dir)
        with open(test_file, 'r') as f:
            document, _ = parser.parse(f)
        files = sorted(document.package.files)
        assert files[0].conc_lics.identifier.toPython() == 'LicenseRef-1'
        assert files[1].conc_lics.identifier == 'Apache-2.0'
