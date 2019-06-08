from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import unittest
from unittest import TestCase

from spdx import config
from spdx.version import Version

class TestLicenseList(TestCase):

    def test_load_license_list(self):
        version, licenses_map = config.load_license_list(config._licenses)
        assert version == '3.5'
        # Test some instances in licenses_map
        assert licenses_map['MIT License'] == 'MIT'
        assert licenses_map['MIT'] == 'MIT License'
        assert licenses_map['Apache License 2.0'] == 'Apache-2.0'
        assert licenses_map['Apache-2.0'] == 'Apache License 2.0'
        assert licenses_map['GNU General Public License v3.0 only'] == 'GPL-3.0-only'
        assert licenses_map['GPL-3.0-only'] == 'GNU General Public License v3.0 only'
    
    def test_config_license_list_version_constant(self):
        assert config.LICENSE_LIST_VERSION == Version(major=3, minor=5)

    def test_load_exception_list(self):
        version, exception_map = config.load_exception_list(config._exceptions)
        assert version == '3.5'
        # Test some instances in exception_map
        assert exception_map['Bison exception 2.2'] == 'Bison-exception-2.2'
        assert exception_map['Bison-exception-2.2'] == 'Bison exception 2.2'
        assert exception_map['OpenVPN OpenSSL Exception'] == 'openvpn-openssl-exception'
        assert exception_map['openvpn-openssl-exception'] == 'OpenVPN OpenSSL Exception'
        assert exception_map['Qt GPL exception 1.0'] == 'Qt-GPL-exception-1.0'
        assert exception_map['Qt-GPL-exception-1.0'] == 'Qt GPL exception 1.0'
    
    def test_config_exception_list_version_constant(self):
        assert config.EXCEPTION_LIST_VERSION == Version(major=3, minor=5)


if __name__ == '__main__':
    unittest.main()
