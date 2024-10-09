# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx.writer.rdf.writer_utils import add_namespace_to_spdx_id


@pytest.mark.parametrize(
    "spdx_id,namespace,external_namespaces,expected",
    [
        ("SPDXRef-File", "docNamespace", {}, "docNamespace#SPDXRef-File"),
        (
            "externalDoc:SPDXRef-File",
            "docNamespace",
            {"externalDoc": "externalNamespace"},
            "externalNamespace#SPDXRef-File",
        ),
        ("externalDoc#A-Ref", "", {}, "externalDoc#A-Ref"),
        ("externalDoc:A-Ref", "", {}, "externalDoc:A-Ref"),
    ],
)
def test_add_namespace_to_spdx_id(spdx_id, namespace, expected, external_namespaces):
    extended_spdx_id = add_namespace_to_spdx_id(spdx_id, namespace, external_namespaces)

    assert extended_spdx_id == expected
