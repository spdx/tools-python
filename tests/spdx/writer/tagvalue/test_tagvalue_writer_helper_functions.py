# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest.mock import MagicMock, call, mock_open, patch

import pytest

from spdx_tools.spdx.model import ActorType, RelationshipType, SpdxNoAssertion
from spdx_tools.spdx.writer.tagvalue.tagvalue_writer_helper_functions import scan_relationships, write_actor
from tests.spdx.fixtures import actor_fixture, file_fixture, package_fixture, relationship_fixture


def test_scan_relationships():
    first_package_spdx_id = "SPDXRef-Package1"
    second_package_spdx_id = "SPDXRef-Package2"
    packages = [package_fixture(spdx_id=first_package_spdx_id), package_fixture(spdx_id=second_package_spdx_id)]
    file_spdx_id = "SPDXRef-File"
    files = [file_fixture(spdx_id=file_spdx_id)]
    relationships = [
        relationship_fixture(
            spdx_element_id=first_package_spdx_id,
            relationship_type=RelationshipType.CONTAINS,
            related_spdx_element_id=file_spdx_id,
            comment=None,
        ),
        relationship_fixture(
            spdx_element_id=second_package_spdx_id,
            relationship_type=RelationshipType.CONTAINS,
            related_spdx_element_id=file_spdx_id,
            comment=None,
        ),
    ]

    relationships_to_write, contained_files_by_package_id = scan_relationships(relationships, packages, files)

    assert relationships_to_write == []
    assert contained_files_by_package_id == {first_package_spdx_id: files, second_package_spdx_id: files}


@pytest.mark.parametrize(
    "element_to_write, expected_calls",
    [
        (actor_fixture(), [call("ActorTest: Person: actorName (some@mail.com)\n")]),
        (
            actor_fixture(actor_type=ActorType.ORGANIZATION, name="organizationName"),
            [call("ActorTest: Organization: organizationName (some@mail.com)\n")],
        ),
        (actor_fixture(actor_type=ActorType.TOOL, name="toolName", email=None), [call("ActorTest: Tool: toolName\n")]),
        (SpdxNoAssertion(), [call("ActorTest: NOASSERTION\n")]),
    ],
)
def test_write_actor(element_to_write, expected_calls):
    mock: MagicMock = mock_open()
    with patch(f"{__name__}.open", mock, create=True):
        with open("foo", "w") as file:
            write_actor("ActorTest", element_to_write, file)

    mock.assert_called_once_with("foo", "w")
    handle = mock()
    handle.write.assert_has_calls(expected_calls)
