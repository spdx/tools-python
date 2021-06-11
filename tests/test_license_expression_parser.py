from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import unittest
from unittest import TestCase

from spdx.parsers.tagvalue import Parser
from spdx.parsers.tagvaluebuilders import Builder
from spdx.parsers.loggers import StandardLogger

from license_expression import LicenseSymbol
from license_expression import LicenseWithExceptionSymbol

class LicenseExpressionParser(TestCase):

    def setUp(self):
        self.tagvalue_parser = Parser(Builder(), StandardLogger())
        self.tagvalue_parser.build()
        self.license_parser = self.tagvalue_parser.license_expression_parser
    
    def test_load_symbols(self):
        symbols = self.license_parser.known_symbols

        result = [
            symbols['BSD-3-Clause'], 
            symbols['CC-BY-1.0'], 
            symbols['MIT'], 
            symbols['OSL-1.1'], 
            symbols['Python-2.0'], 
            symbols['Autoconf-exception-3.0'], 
            symbols['Classpath-exception-2.0'], 
            symbols['GCC-exception-3.1'], 
            symbols['Linux-syscall-note'],
            symbols['Autoconf-exception-3.0']
        ]
        expected = [
            LicenseSymbol('BSD-3-Clause'),
            LicenseSymbol('CC-BY-1.0'),
            LicenseSymbol('MIT'),
            LicenseSymbol('OSL-1.1'),
            LicenseSymbol('Python-2.0'),
            LicenseSymbol('Autoconf-exception-3.0', is_exception=True),
            LicenseSymbol('Classpath-exception-2.0', is_exception=True),
            LicenseSymbol('GCC-exception-3.1', is_exception=True),
            LicenseSymbol('Linux-syscall-note', is_exception=True),
            LicenseSymbol('Autoconf-exception-3.0', is_exception=True)
        ]

        assert result == expected
    
    def test_parse_simple_expression(self):
        expression = '(LicenseRef-3 AND LicenseRef-4 AND Apache-1.0 AND Apache-2.0 AND MPL-1.1 AND LicenseRef-1 AND LicenseRef-2)'
        result = self.license_parser.parse(expression)

        result_symbols = result.symbols
        expected_symbols = {
            LicenseSymbol('LicenseRef-3'), 
            LicenseSymbol('LicenseRef-4'), 
            LicenseSymbol('Apache-1.0'), 
            LicenseSymbol('Apache-2.0'), 
            LicenseSymbol('MPL-1.1'), 
            LicenseSymbol('LicenseRef-1'), 
            LicenseSymbol('LicenseRef-2')
        }
        
        result_unknown_symbols = self.license_parser.unknown_license_symbols(result)
        expected_unknown_symbols = [
            LicenseSymbol('LicenseRef-3'), 
            LicenseSymbol('LicenseRef-4'), 
            LicenseSymbol('LicenseRef-1'), 
            LicenseSymbol('LicenseRef-2')
        ]

        assert result_symbols == expected_symbols
        assert result_unknown_symbols == expected_unknown_symbols

    def test_parse_expression_with_exception(self):
        expression = '(GPL-2.0-or-later WITH Classpath-exception-2.0 AND MIT) OR (LPL-1.0 AND MIT) OR LicenseRef-1'
        result = self.license_parser.parse(expression)

        result_symbols = result.symbols
        expected_symbols = {
            LicenseWithExceptionSymbol(
                LicenseSymbol('GPL-2.0-or-later'), 
                LicenseSymbol('Classpath-exception-2.0', is_exception=True)
            ), 
            LicenseSymbol('MIT'), 
            LicenseSymbol('LPL-1.0'), 
            LicenseSymbol('MIT'), 
            LicenseSymbol('LicenseRef-1')
        }
        
        result_unknown_symbols = self.license_parser.unknown_license_symbols(result)
        expected_unknown_symbols = [
            LicenseSymbol('LicenseRef-1')
        ]

        assert result_symbols == expected_symbols
        assert result_unknown_symbols == expected_unknown_symbols


if __name__ == '__main__':
    unittest.main()
