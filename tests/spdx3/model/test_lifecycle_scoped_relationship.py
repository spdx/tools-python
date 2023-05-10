# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime
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
        RelationshipType.DESCRIBES,
        ["spdx_id2", "spdx_id3"],
        completeness=RelationshipCompleteness.NOASSERTION,
        start_time=datetime(11, 11, 11),
        end_time=datetime(12, 12, 12),
        scope=LifecycleScopeType.DESIGN,
    )

    assert relationship.spdx_id == "SPDXRef-Relationship"
    assert relationship.creation_info == creation_information
    assert relationship.from_element == "spdx_id1"
    assert relationship.to == ["spdx_id2", "spdx_id3"]
    assert relationship.relationship_type == RelationshipType.DESCRIBES
    assert relationship.completeness == RelationshipCompleteness.NOASSERTION
    assert relationship.start_time == datetime(11, 11, 11)
    assert relationship.end_time == datetime(12, 12, 12)
    assert relationship.scope == LifecycleScopeType.DESIGN


@mock.patch("spdx_tools.spdx3.model.CreationInformation", autospec=True)
def test_invalid_initialization(creation_information):
    with pytest.raises(TypeError) as err:
        LifecycleScopedRelationship(
            "SPDXRef-Relationship",
            creation_information,
            "spdx_id1",
            RelationshipType.DESCRIBES,
            42,
        )

    assert err.value.args[0] == [
        'SetterError LifecycleScopedRelationship: type of argument "to" must be a ' "list; got int instead: 42"
    ]
