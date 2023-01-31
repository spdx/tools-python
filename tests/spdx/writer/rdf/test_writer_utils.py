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

from spdx.writer.rdf.writer_utils import add_namespace_to_spdx_id


@pytest.mark.parametrize("spdx_id,namespace,external_namespaces,expected",
                         [("SPDXRef-File", "docNamespace", {}, "docNamespace#SPDXRef-File"),
                          ("externalDoc:SPDXRef-File", "docNamespace", {"externalDoc": "externalNamespace"},
                           "externalNamespace#SPDXRef-File"),
                          ("externalDoc#A-Ref", "", {}, "externalDoc#A-Ref"),
                          ("externalDoc:A-Ref", "", {}, "externalDoc:A-Ref")])
def test_add_namespace_to_spdx_id(spdx_id, namespace, expected, external_namespaces):
    extended_spdx_id = add_namespace_to_spdx_id(spdx_id, namespace, external_namespaces)

    assert extended_spdx_id == expected
