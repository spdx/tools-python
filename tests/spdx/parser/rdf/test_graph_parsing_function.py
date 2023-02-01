# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pytest
from rdflib import URIRef

from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.model.spdx_none import SpdxNone
from spdx.parser.rdf.graph_parsing_functions import str_to_no_assertion_or_none, parse_spdx_id


@pytest.mark.parametrize("value,expected",[("NOASSERTION", SpdxNoAssertion()), ("NONE", SpdxNone()), ("test", "test"),
                                           ("Noassertion", "Noassertion")])
def test_str_to_no_assertion_or_none(value, expected):
    result = str_to_no_assertion_or_none(value)

    assert result == expected

@pytest.mark.parametrize("resource,doc_namespace,"
                         "expected", [(URIRef("docNamespace#SPDXRef-Test"), "docNamespace", "SPDXRef-Test"),
                                      (URIRef("docNamespaceSPDXRef-Test"), "docNamespace", "docNamespaceSPDXRef-Test"),
                                      (URIRef("differentNamespace#SPDXRef-Test"), "docNamespace", "differentNamespace#SPDXRef-Test"),
                                      (None, "", None),])
def test_parse_spdx_id(resource, doc_namespace, expected):
    spdx_id = parse_spdx_id(resource, doc_namespace)

    assert spdx_id == expected
