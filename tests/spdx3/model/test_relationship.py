# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime
from unittest import mock

import pytest

from spdx3.fixtures import relationship_fixture, ELEMENT_DICT, RELATIONSHIP_DICT
from spdx_tools.spdx3.model import Relationship, RelationshipCompleteness, RelationshipType


@mock.patch("spdx_tools.spdx3.model.CreationInformation", autospec=True)
def test_correct_initialization(creation_information):
    relationship = relationship_fixture()

    local_dict = {}
    local_dict.update(ELEMENT_DICT)
    local_dict.update(RELATIONSHIP_DICT)
    local_dict["spdx_id"] = "https://spdx.test/tools-python/relationship_fixture"

    keys  = [
        attribute
        for attribute in dir(Relationship)
        if isinstance(getattr(Relationship, attribute), property)
    ]

    for key in keys:
        assert getattr(relationship, key) is not None
        assert getattr(relationship, key) == local_dict[key]

    # assert relationship.spdx_id == "SPDXRef-Relationship"
    # assert relationship.creation_info == creation_information
    # assert relationship.from_element == "spdx_id1"
    # assert relationship.to == ["spdx_id2", "spdx_id3"]
    # assert relationship.relationship_type == RelationshipType.DESCRIBES
    # assert relationship.completeness == RelationshipCompleteness.NOASSERTION
    # assert relationship.start_time == datetime(11, 11, 11)
    # assert relationship.end_time == datetime(12, 12, 12)


@mock.patch("spdx_tools.spdx3.model.CreationInformation", autospec=True)
def test_invalid_initialization(creation_information):
    with pytest.raises(TypeError) as err:
        Relationship("SPDXRef-Relationship", creation_information, 42, "Relationshiptype", 5, completeness=True)

    assert err.value.args[0] == [
        'SetterError Relationship: type of argument "from_element" must be ' "str; got int instead: 42",
        'SetterError Relationship: type of argument "to" must be a list; got int ' "instead: 5",
        'SetterError Relationship: type of argument "relationship_type" must be '
        "spdx_tools.spdx3.model.relationship.RelationshipType; got str instead: Relationshiptype",
        'SetterError Relationship: type of argument "completeness" must be one of '
        "(spdx_tools.spdx3.model.relationship.RelationshipCompleteness, NoneType); got bool "
        "instead: True",
    ]
