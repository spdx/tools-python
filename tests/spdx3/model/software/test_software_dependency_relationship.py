# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime
from unittest import mock

import pytest

from spdx_tools.spdx3.model import LifecycleScopeType, RelationshipCompleteness, RelationshipType
from spdx_tools.spdx3.model.software import (
    DependencyConditionalityType,
    SoftwareDependencyLinkType,
    SoftwareDependencyRelationship,
)


@mock.patch("spdx_tools.spdx3.model.CreationInfo", autospec=True)
def test_correct_initialization(creation_info):
    relationship = SoftwareDependencyRelationship(
        "SPDXRef-Relationship",
        "spdx_id1",
        RelationshipType.DESCRIBES,
        ["spdx_id2", "spdx_id3"],
        creation_info=creation_info,
        completeness=RelationshipCompleteness.NOASSERTION,
        start_time=datetime(11, 11, 11),
        end_time=datetime(12, 12, 12),
        scope=LifecycleScopeType.DESIGN,
        software_linkage=SoftwareDependencyLinkType.STATIC,
        conditionality=DependencyConditionalityType.PROVIDED,
    )

    assert relationship.spdx_id == "SPDXRef-Relationship"
    assert relationship.creation_info == creation_info
    assert relationship.from_element == "spdx_id1"
    assert relationship.to == ["spdx_id2", "spdx_id3"]
    assert relationship.relationship_type == RelationshipType.DESCRIBES
    assert relationship.completeness == RelationshipCompleteness.NOASSERTION
    assert relationship.start_time == datetime(11, 11, 11)
    assert relationship.end_time == datetime(12, 12, 12)
    assert relationship.scope == LifecycleScopeType.DESIGN
    assert relationship.software_linkage == SoftwareDependencyLinkType.STATIC
    assert relationship.conditionality == DependencyConditionalityType.PROVIDED


@mock.patch("spdx_tools.spdx3.model.CreationInfo", autospec=True)
def test_invalid_initialization(creation_info):
    with pytest.raises(TypeError) as err:
        SoftwareDependencyRelationship(
            "SPDXRef-Relationship",
            "spdx_id1",
            RelationshipType.DESCRIBES,
            to=42,
            creation_info=creation_info,
        )

    assert len(err.value.args[0]) == 1
    for error in err.value.args[0]:
        assert error.startswith("SetterError SoftwareDependencyRelationship:")
