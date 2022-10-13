# Copyright (c) 2022 spdx tool contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from unittest import TestCase

from spdx.cli_tools.convertor import determine_infile_and_outfile

from tests.testing_utils import raises


class TestConvertor(TestCase):
    maxDiff = None

    def test_determine_input_with_known_i_o_format(self):
        infile_given = 'infile.rdf'
        outfile_given = 'outfile.json'
        src = ()
        from_ = None
        to = None

        infile, outfile = determine_infile_and_outfile(infile_given, outfile_given, src, from_, to)

        assert infile == infile_given
        assert outfile == outfile_given

    def test_determine_input_with_unknown_i_o_format(self):
        infile_given = None
        outfile_given = None
        src = ('infile.in', 'outfile.out')
        from_ = 'rdf'
        to = 'json'
        expected_infile = 'infile.rdf'
        expected_outfile = 'outfile.json'

        infile, outfile = determine_infile_and_outfile(infile_given, outfile_given, src, from_, to)

        assert infile == expected_infile
        assert outfile == expected_outfile

    def test_determine_input_with_known_i_format_unknown_o_format(self):
        infile_given = 'infile.rdf'
        outfile_given = None
        src = ('outfile',)
        from_ = None
        to = 'json'
        expected_outfile = 'outfile.json'

        infile, outfile = determine_infile_and_outfile(infile_given, outfile_given, src, from_, to)

        assert infile == infile_given
        assert outfile == expected_outfile

    def test_determine_input_with_unknown_i_format_known_o_format(self):
        infile_given = None
        outfile_given = 'outfile.json'
        src = ('infile',)
        from_ = 'rdf'
        to = None
        expected_infile = 'infile.rdf'

        infile, outfile = determine_infile_and_outfile(infile_given, outfile_given, src, from_, to)

        assert infile == expected_infile
        assert outfile == outfile_given

    @raises(ValueError)
    def test_determine_input_with_invalid_arguments(self):
        infile_given = None
        outfile_given = None
        src = ()
        from_ = None
        to = None

        infile, outfile = determine_infile_and_outfile(infile_given, outfile_given, src, from_, to)
