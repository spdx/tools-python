# Copyright (c) 2014 Ahmed H. Ismail
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
from unittest import TestCase

from spdx.checksum import Checksum
from spdx.package import Package


class TestPackage(TestCase):

    @unittest.skip("https://github.com/spdx/tools-python/issues/296")
    def test_calc_verif_code(self):
        package = Package()
        package.calc_verif_code()

    def test_package_with_non_sha1_check_sum(self):
        package = Package()
        package.set_checksum(Checksum("SHA256", ''))

        # Make sure that validation still works despite the checksum not being SHA1
        messages = []
        package.validate_checksums(messages)


if __name__ == '__main__':
    unittest.main()
