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
import json
import os

import pytest
from spdx.parsers import parse_anything
from spdx.utils import UnKnown
from spdx.writers import write_anything

from tests import utils_test


dirname = os.path.join(os.path.dirname(__file__), "data", "formats")
test_files = [os.path.join(dirname, fn) for fn in os.listdir(dirname)]
# narrow this list to the current version only.
version = 'v2.3'
version_files = []
for test_file in test_files:
    if version in test_file:
        version_files.append(test_file)
test_files = version_files

UNSTABLE_CONVERSIONS = {
    "SPDXTagExample-v2.3.spdx-rdf",
    "SPDXTagExample-v2.3.spdx-yaml",
    "SPDXTagExample-v2.3.spdx-xml",
    "SPDXTagExample-v2.3.spdx-json",
    "SPDXSimpleTag.tag-rdf",
    "SPDXXMLExample-v2.3.spdx.xml-rdf",
    "SPDXXMLExample-v2.3.spdx.xml-tag",
    "SPDXJSONExample-V2.3.spdx.json-rdf",
    "SPDXJSONExample-V2.3.spdx.json-tag",
    "SPDXYAMLExample-v2.3.spdx.yaml-rdf",
    "SPDXYAMLExample-v2.3.spdx.yaml-tag",
    "SPDXRdfExample-v2.3.spdx.rdf-rdf",
    "SPDXRdfExample-v2.3.spdx.rdf-yaml",
    "SPDXRdfExample-v2.3.spdx.rdf-xml",
    "SPDXRdfExample-v2.3.spdx.rdf-json",
    "SPDXRdfExample-v2.3.spdx.rdf-tag",
}


def handle_unserializable(obj):
    if isinstance(obj, UnKnown):
        return obj.to_value()
    return obj


@pytest.mark.parametrize("out_format", ['rdf', 'yaml', 'xml', 'json', 'tag'])
@pytest.mark.parametrize("in_file", test_files, ids=lambda x: os.path.basename(x))
def test_write_anything(in_file, out_format, tmpdir):
    in_basename = os.path.basename(in_file)
    if in_basename == "SPDXSBOMExample.spdx.yml":
        # conversion of spdx2.2 is not yet done
        return
    doc, error = parse_anything.parse_file(in_file)

    assert not error
    expected_dict = utils_test.TestParserUtils.to_dict(doc)

    out_fn = os.path.join(tmpdir, "test." + out_format)
    write_anything.write_file(doc, out_fn)

    doc2, error2 = parse_anything.parse_file(out_fn)
    assert not error2

    written_file_dict = utils_test.TestParserUtils.to_dict(doc2)

    try:
        expected_json = json.dumps(expected_dict, sort_keys=True, indent=2, default=handle_unserializable)
    except TypeError:
        expected_json = None
    try:
        written_file_json = json.dumps(written_file_dict, sort_keys=True, indent=2, default=handle_unserializable)
    except TypeError:
        written_file_json = None

    assert written_file_json is not None

    test = in_basename + "-" + out_format
    if test not in UNSTABLE_CONVERSIONS:
        if written_file_json != expected_json:
            print('uhoh')
        assert expected_json == written_file_json
    else:
        # if this test fails, this means we are more stable \o/
        # in that case, please remove the test from UNSTABLE_CONVERSIONS list
        assert expected_json != written_file_json, test

