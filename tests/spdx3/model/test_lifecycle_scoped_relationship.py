# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import mock

import pytest

from spdx_tools.spdx3.model import (
    LifecycleScopedRelationship,
    LifecycleScopeType,
    RelationshipCompleteness,
    RelationshipType,
)


@mock.patch("spdx_tools.spdx3.model.CreationInformation", autospec=True)
def test_correct_initialization(creation_information):
    relationship = LifecycleScopedRelationship(
        "SPDXRef-Relationship",
        creation_information,
        "spdx_id1",
        ["spdx_id2", "spdx_id3"],
        RelationshipType.DESCRIBES,
        completeness=RelationshipCompleteness.NOASSERTION,
        scope=LifecycleScopeType.DESIGN,
    )

    assert relationship.spdx_id == "SPDXRef-Relationship"
    assert relationship.creation_info == creation_information
    assert relationship.from_element == "spdx_id1"
    assert relationship.to == ["spdx_id2", "spdx_id3"]
    assert relationship.relationship_type == RelationshipType.DESCRIBES
    assert relationship.completeness == RelationshipCompleteness.NOASSERTION
    assert relationship.scope == LifecycleScopeType.DESIGN


@mock.patch("spdx_tools.spdx3.model.CreationInformation", autospec=True)
def test_invalid_initialization(creation_information):
    with pytest.raises(TypeError) as err:
        LifecycleScopedRelationship(
            "SPDXRef-Relationship",
            creation_information,
            "spdx_id1",
            42,
            RelationshipType.DESCRIBES,
        )

    assert err.value.args[0] == [
        'SetterError LifecycleScopedRelationship: type of argument "to" must be a ' "list; got int instead: 42"
    ]
