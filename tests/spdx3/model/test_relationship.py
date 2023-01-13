# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from unittest import mock

import pytest

from spdx3.model.element import Element

from spdx3.model.relationship import Relationship, RelationshipType, RelationshipCompleteness


@mock.patch("spdx3.model.creation_information.CreationInformation")
def test_correct_initialization(creation_information):
    element = Element("SPDXRef-Element",
                      creation_info=creation_information)  # using a mock here leads to failure as check_types_and_set_values accesses the element class

    relationship = Relationship("SPDXRef-Relationship", creation_information, element, [element, element],
                                RelationshipType.DESCRIBES, completeness=RelationshipCompleteness.UNKNOWN)

    assert relationship.spdx_id == "SPDXRef-Relationship"
    assert relationship.creation_info == creation_information
    assert relationship.from_element == element
    assert relationship.to == [element, element]
    assert relationship.relationship_type == RelationshipType.DESCRIBES
    assert relationship.completeness == RelationshipCompleteness.UNKNOWN


@mock.patch("spdx3.model.creation_information.CreationInformation")
def test_invalid_initialization(creation_information):
    with pytest.raises(TypeError) as err:
        Relationship("SPDXRef-Relationship", creation_information, "Element", 5, "Relationshiptype", completeness=True)

    assert err.value.args[0] == ['SetterError Relationship: type of argument "from_element" must be '
                                 'spdx3.model.element.Element; got str instead: Element',
                                 'SetterError Relationship: type of argument "to" must be a list; got int '
                                 'instead: 5',
                                 'SetterError Relationship: type of argument "relationship_type" must be '
                                 'spdx3.model.relationship.RelationshipType; got str instead: Relationshiptype',
                                 'SetterError Relationship: type of argument "completeness" must be one of '
                                 '(spdx3.model.relationship.RelationshipCompleteness, NoneType); got bool '
                                 'instead: True']
