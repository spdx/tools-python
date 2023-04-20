# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import mock

import pytest

from spdx_tools.spdx3.model import Relationship, RelationshipCompleteness, RelationshipType


@mock.patch("spdx_tools.spdx3.model.CreationInformation", autospec=True)
def test_correct_initialization(creation_information):
    relationship = Relationship(
        "SPDXRef-Relationship",
        creation_information,
        "spdx_id1",
        ["spdx_id2", "spdx_id3"],
        RelationshipType.DESCRIBES,
        completeness=RelationshipCompleteness.UNKNOWN,
    )

    assert relationship.spdx_id == "SPDXRef-Relationship"
    assert relationship.creation_info == creation_information
    assert relationship.from_element == "spdx_id1"
    assert relationship.to == ["spdx_id2", "spdx_id3"]
    assert relationship.relationship_type == RelationshipType.DESCRIBES
    assert relationship.completeness == RelationshipCompleteness.UNKNOWN


@mock.patch("spdx_tools.spdx3.model.CreationInformation", autospec=True)
def test_invalid_initialization(creation_information):
    with pytest.raises(TypeError) as err:
        Relationship("SPDXRef-Relationship", creation_information, 42, 5, "Relationshiptype", completeness=True)

    assert err.value.args[0] == [
        'SetterError Relationship: type of argument "from_element" must be ' "str; got int instead: 42",
        'SetterError Relationship: type of argument "to" must be a list; got int ' "instead: 5",
        'SetterError Relationship: type of argument "relationship_type" must be '
        "spdx_tools.spdx3.model.relationship.RelationshipType; got str instead: Relationshiptype",
        'SetterError Relationship: type of argument "completeness" must be one of '
        "(spdx_tools.spdx3.model.relationship.RelationshipCompleteness, NoneType); got bool "
        "instead: True",
    ]
