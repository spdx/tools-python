import unittest
import re
from unittest import TestCase
from spdx.parsers.rdf import Parser
from spdx.parsers.rdfbuilders import Builder
from spdx.parsers.loggers import StandardLogger
from tests import utils_test

class TestParser(TestCase):

    def test_extracted_licenses(self):
        parser = Parser(Builder(), StandardLogger())
        test_file = utils_test.get_test_loc('../../data/SPDXRdfExample.rdf', test_data_dir=utils_test.test_data_dir)
        with open(test_file, 'r') as file:
            document, _ = parser.parse(file)
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
        with open(test_file, 'r') as file:
            document, _ = parser.parse(file)
        # It is needed to ckeck it as sorted lists because the order changes when parsing
        lic_expected = ['Apache-2.0', 'LicenseRef-1', 'LicenseRef-2', 'LicenseRef-3', 'LicenseRef-4', 'MPL-1.1']
        lic_result = sorted(document.package.license_declared.identifier.split(' AND '))
        assert lic_result == lic_expected
    
    def test_pkg_lic_conc(self):
        parser = Parser(Builder(), StandardLogger())
        test_file = utils_test.get_test_loc('../../data/SPDXRdfExample.rdf', test_data_dir=utils_test.test_data_dir)
        with open(test_file, 'r') as file:
            document, _ = parser.parse(file)
        # It is needed to ckeck it as sorted lists because the order changes when parsing
        lic_expected = ['Apache-1.0', 'Apache-2.0', 'LicenseRef-1', 'LicenseRef-2', 'LicenseRef-3', 'LicenseRef-4', 'MPL-1.1']
        lic_result = sorted(document.package.conc_lics.identifier.split(' AND '))
        assert lic_result == lic_expected
    
    def test_file_lic_conc(self):
        parser = Parser(Builder(), StandardLogger())
        test_file = utils_test.get_test_loc('../../data/SPDXRdfExample.rdf', test_data_dir=utils_test.test_data_dir)
        with open(test_file, 'r') as file:
            document, _ = parser.parse(file)
        files = sorted(document.package.files)
        assert files[0].conc_lics.identifier.toPython() == 'LicenseRef-1'
        assert files[1].conc_lics.identifier == 'Apache-2.0'

if __name__ == '__main__':
    unittest.main()
