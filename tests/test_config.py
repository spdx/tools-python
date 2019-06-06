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
        assert version == '2.6'
        # Test some instances in licenses_map
        assert licenses_map['MIT License'] == 'MIT'
        assert licenses_map['MIT'] == 'MIT License'
        assert licenses_map['Apache License 2.0'] == 'Apache-2.0'
        assert licenses_map['Apache-2.0'] == 'Apache License 2.0'
        assert licenses_map['GNU General Public License v3.0 only'] == 'GPL-3.0'
        assert licenses_map['GPL-3.0'] == 'GNU General Public License v3.0 only'
    
    def test_config_license_list_version_constant(self):
        assert config.LICENSE_LIST_VERSION == Version(major=2, minor=6)


if __name__ == '__main__':
    unittest.main()
