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
test_files_json_yaml_xml_tag = [filename for filename in test_files if filename.endswith("json") or
                            filename.endswith("yaml") or filename.endswith("xml") or filename.endswith("tag")]
test_files_rdf = [filename for filename in test_files if filename.endswith("rdf")]
UNSTABLE_CONVERSIONS = {
    "SPDXTagExample.tag-rdf",
    "SPDXTagExample.tag-yaml",
    "SPDXTagExample.tag-xml",
    "SPDXTagExample.tag-json",
    "SPDXSimpleTag.tag-rdf",
    "SPDXXmlExample.xml-rdf",
    "SPDXXmlExample.xml-tag",
    "SPDXJsonExample.json-rdf",
    "SPDXJsonExample.json-tag",
    "SPDXYamlExample.yaml-rdf",
    "SPDXYamlExample.yaml-tag",
    "SPDXRdfExample.rdf-rdf",
    "SPDXRdfExample.rdf-yaml",
    "SPDXRdfExample.rdf-xml",
    "SPDXRdfExample.rdf-json",
    "SPDXRdfExample.rdf-tag",
    "SPDXJsonExample2.2.json-rdf",
    "SPDXJsonExample2.2.json-tag",
}

# Because the rdf-parser/ writer can't handle the mandatory field byte_range in snippets yet we can only test conversion
# from json, yaml, xml and tv to each other format and rdf to rdf. Otherwise, the jsonyamlxml- or tv-writer would add
# the initial value None for snippet_ranges which then leads to an error while parsing.
# https://github.com/spdx/tools-python/issues/274


@pytest.mark.parametrize("out_format", ['rdf', 'yaml', 'xml', 'json', 'tag'])
@pytest.mark.parametrize("in_file", test_files_json_yaml_xml_tag, ids=lambda x: os.path.basename(x))
def test_write_anything_json_yaml_xml_tv(in_file, out_format, tmpdir):
    in_basename = os.path.basename(in_file)
    if in_basename == "SPDXSBOMExample.spdx.yml" or in_basename == "SPDXJsonExample2.2.json" or in_basename == "SPDXSBOMExample.tag":
        # conversion of spdx2.2 is not yet done
        return
    write_anything_test(in_basename, in_file, out_format, tmpdir)


@pytest.mark.parametrize("out_format", ['rdf'])
@pytest.mark.parametrize("in_file", test_files_rdf, ids=lambda x: os.path.basename(x))
def test_write_anything_rdf(in_file, out_format, tmpdir):
    in_basename = os.path.basename(in_file)
    write_anything_test(in_basename, in_file, out_format, tmpdir)


def write_anything_test(in_basename, in_file, out_format, tmpdir):
    doc, error = parse_anything.parse_file(in_file)
    assert not error
    result = utils_test.TestParserUtils.to_dict(doc)
    out_fn = os.path.join(tmpdir, "test." + out_format)
    write_anything.write_file(doc, out_fn)
    doc2, error2 = parse_anything.parse_file(out_fn)
    result2 = utils_test.TestParserUtils.to_dict(doc2)
    assert not error2
    test = in_basename + "-" + out_format
    if test not in UNSTABLE_CONVERSIONS:
        assert result == result2
    else:
        # if this test fails, this means we are more stable \o/
        # in that case, please remove the test from UNSTABLE_CONVERSIONS list
        assert result2 != result, test
