# Copyright (c) 2021 spdx tool contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import, print_function, unicode_literals

import os

import pytest
from spdx.parsers import parse_anything
from spdx.writers import write_anything

from tests import utils_test

dirname = os.path.join(os.path.dirname(__file__), "data", "formats")
test_files = [os.path.join(dirname, fn) for fn in os.listdir(dirname)]
UNSTABLE_CONVERSIONS = [
    "rdf->rdf",
    "yaml->rdf",
    "xml->rdf",
    "json->rdf",
    "tag->rdf",
    "rdf->yaml",
    "tag->yaml",
    "rdf->xml",
    "tag->xml",
    "rdf->json",
    "tag->json",
    "rdf->tag",
    "yaml->tag",
    "xml->tag",
    "json->tag",
]

@pytest.mark.parametrize("in_format", ['rdf', 'yaml', 'xml', 'json', 'tag'])
@pytest.mark.parametrize("out_format", ['rdf', 'yaml', 'xml', 'json', 'tag'])
def test_write_anything(in_format, out_format, tmpdir):

    for in_file in test_files:
        if in_file.endswith(in_format):
            break
    doc, error = parse_anything.parse_file(in_file)

    assert not error
    result = utils_test.TestParserUtils.to_dict(doc)

    out_fn = os.path.join(tmpdir, "test." + out_format)
    write_anything.write_file(doc, out_fn)

    doc2, error2 = parse_anything.parse_file(out_fn)
    result2 = utils_test.TestParserUtils.to_dict(doc2)
    assert not error2
    
    test = in_format + "->" + out_format
    if test not in UNSTABLE_CONVERSIONS:
        for k, v in result.items():
            assert v == result2[k], k + " differs"
    else:
        # if this test fails, this means we are more stable \o/
        # in that case, please remove the test from UNSTABLE_CONVERSIONS list
        assert result2 != result, test

