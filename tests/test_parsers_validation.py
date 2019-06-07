
# Copyright (c) SPDX Python tools authors
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

from unittest import TestCase

from spdx.parsers import validations
from spdx import utils


class TestValidations(TestCase):

    def test_validate_pkg_cr_text_does_not_crash_on_None(self):
        validations.validate_pkg_cr_text(None)

    def test_validate_pkg_cr_text_does_not_crash_on_NoAssert_or_SPDXNone(self):
        validations.validate_pkg_cr_text(utils.NoAssert())
        validations.validate_pkg_cr_text(utils.SPDXNone())

    def test_validate_file_cpyright_does_not_crash_on_None(self):
        validations.validate_file_cpyright(None)

    def test_validate_file_cpyright_does_not_crash_on_NoAssert_or_SPDXNone(self):
        validations.validate_file_cpyright(utils.NoAssert())
        validations.validate_file_cpyright(utils.SPDXNone())
