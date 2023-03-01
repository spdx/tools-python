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

import os

import pytest

from spdx.parsers import parse_anything
from spdx.writers import write_anything
from tests import utils_test

dirname = os.path.join(os.path.dirname(__file__), "data", "formats")
test_files = [os.path.join(dirname, fn) for fn in os.listdir(dirname)]
test_files_json_yaml_xml_tag = [filename for filename in test_files if filename.endswith("json")
                                or filename.endswith("yaml") or filename.endswith("xml") or filename.endswith("tag")]
test_files_rdf = [filename for filename in test_files if filename.endswith("rdf")]
UNSTABLE_CONVERSIONS = {
    "SPDXTagExample.tag-yaml",
    "SPDXTagExample.tag-xml",
    "SPDXTagExample.tag-json",
    "SPDXXmlExample.xml-tag",
    "SPDXJsonExample.json-tag",
    "SPDXYamlExample.yaml-tag",
    "SPDXRdfExample.rdf-rdf",
    "SPDXYAMLExample-2.2.spdx.yaml-tag",
    "SPDXJSONExample-v2.2.spdx.json-tag",
    "SPDXXMLExample-v2.2.spdx.xml-tag",
    "SPDXYAMLExample-2.3.spdx.yaml-tag",
    "SPDXJSONExample-v2.3.spdx.json-tag",
    "SPDXXMLExample-v2.3.spdx.xml-tag"
}


# Because the rdf-parser/ writer can't handle the mandatory field byte_range in snippets yet we can only test conversion
# from json, yaml, xml and tv to each other format and rdf to rdf. Otherwise, the jsonyamlxml- or tv-writer would add
# the initial value None for snippet_ranges which then leads to an error while parsing.
# https://github.com/spdx/tools-python/issues/274


@pytest.mark.parametrize("out_format", ['yaml', 'xml', 'json', 'tag'])
@pytest.mark.parametrize("in_file", test_files_json_yaml_xml_tag, ids=lambda x: os.path.basename(x))
def test_write_anything_json_yaml_xml_tv(in_file, out_format, tmpdir):
    in_basename = os.path.basename(in_file)
    write_anything_test(in_basename, in_file, out_format, tmpdir)


@pytest.mark.parametrize("out_format", ['rdf'])
@pytest.mark.parametrize("in_file", test_files_rdf, ids=lambda x: os.path.basename(x))
def test_write_anything_rdf(in_file, out_format, tmpdir):
    in_basename = os.path.basename(in_file)
    write_anything_test(in_basename, in_file, out_format, tmpdir)


def write_anything_test(in_basename, in_file, out_format, tmpdir):
    """This parses the in_file and writes it to the out_format,
    then parses the written out_file again and checks if it is still the same as in_file."""
    doc_in, error_in = parse_anything.parse_file(in_file)
    assert not error_in
    result_in = utils_test.TestParserUtils.to_dict(doc_in)

    out_file_name = os.path.join(tmpdir, "test." + out_format)
    write_anything.write_file(doc_in, out_file_name)

    doc_out, error_out = parse_anything.parse_file(out_file_name)
    assert not error_out
    result_out = utils_test.TestParserUtils.to_dict(doc_out)

    test = in_basename + "-" + out_format
    if test not in UNSTABLE_CONVERSIONS:
        assert result_in == result_out

    else:
        # if this test fails, this means we are more stable \o/
        # in that case, please remove the test from UNSTABLE_CONVERSIONS list
        assert result_out != result_in, test
