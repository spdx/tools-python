# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest.mock import MagicMock, call, mock_open, patch

import pytest

from spdx_tools.spdx.model import SpdxNoAssertion, SpdxNone
from spdx_tools.spdx.writer.tagvalue.relationship_writer import write_relationship
from tests.spdx.fixtures import relationship_fixture


@pytest.mark.parametrize(
    "relationship, expected_calls",
    [
        (
            relationship_fixture(),
            [
                call("Relationship: SPDXRef-DOCUMENT DESCRIBES SPDXRef-File\n"),
                call("RelationshipComment: relationshipComment\n"),
            ],
        ),
        (
            relationship_fixture(related_spdx_element_id=SpdxNoAssertion(), comment=None),
            [call("Relationship: SPDXRef-DOCUMENT DESCRIBES NOASSERTION\n")],
        ),
        (
            relationship_fixture(
                spdx_element_id="DocumentRef-External:SPDXRef-DOCUMENT",
                related_spdx_element_id=SpdxNone(),
                comment=None,
            ),
            [call("Relationship: DocumentRef-External:SPDXRef-DOCUMENT DESCRIBES NONE\n")],
        ),
    ],
)
def test_relationship_writer(relationship, expected_calls):
    mock: MagicMock = mock_open()
    with patch(f"{__name__}.open", mock, create=True):
        with open("foo", "w") as file:
            write_relationship(relationship, file)

    mock.assert_called_once_with("foo", "w")
    handle = mock()
    handle.write.assert_has_calls(expected_calls)
