# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import mock

from spdx_tools.spdx3.bump_from_spdx2.relationship import bump_relationship, bump_relationships
from spdx_tools.spdx3.model import Relationship, RelationshipCompleteness, RelationshipType
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx.model import RelationshipType as Spdx2_RelationshipType
from spdx_tools.spdx.model import SpdxNoAssertion, SpdxNone
from tests.spdx.fixtures import relationship_fixture


@mock.patch("spdx_tools.spdx3.model.CreationInfo", autospec=True)
def test_relationship_bump(creation_info):
    spdx2_relationship = relationship_fixture()
    document_namespace = "https://doc.namespace"
    relationship = bump_relationship(spdx2_relationship, creation_info, document_namespace, 1)

    assert relationship == Relationship(
        f"{document_namespace}#SPDXRef-Relationship-1",
        spdx2_relationship.spdx_element_id,
        RelationshipType.DESCRIBES,
        [spdx2_relationship.related_spdx_element_id],
        creation_info=creation_info,
        comment=spdx2_relationship.comment,
    )


@mock.patch("spdx_tools.spdx3.model.CreationInfo", autospec=True)
def test_relationships_bump(creation_info):
    relationships = [
        relationship_fixture(comment=None),
        relationship_fixture(related_spdx_element_id="SPDXRef-Package", comment=None),
    ]
    payload = Payload()
    document_namespace = "https://doc.namespace"
    bump_relationships(relationships, payload, creation_info, document_namespace)

    assert payload.get_element(f"{document_namespace}#SPDXRef-Relationship-1") == Relationship(
        f"{document_namespace}#SPDXRef-Relationship-1",
        relationships[0].spdx_element_id,
        RelationshipType.DESCRIBES,
        [relationships[0].related_spdx_element_id, relationships[1].related_spdx_element_id],
        creation_info=creation_info,
    )


@mock.patch("spdx_tools.spdx3.model.CreationInfo", autospec=True)
def test_relationships_bump_with_setting_completeness(creation_info):
    relationships = [
        relationship_fixture(related_spdx_element_id=SpdxNoAssertion()),
        relationship_fixture(related_spdx_element_id="SPDXRef-Package"),
        relationship_fixture(
            relationship_type=Spdx2_RelationshipType.SPECIFICATION_FOR,
            related_spdx_element_id=SpdxNone(),
            comment=None,
        ),
    ]
    payload = Payload()
    document_namespace = "https://doc.namespace"
    bump_relationships(relationships, payload, creation_info, document_namespace)

    assert payload.get_element(f"{document_namespace}#SPDXRef-Relationship-0") == Relationship(
        f"{document_namespace}#SPDXRef-Relationship-0",
        relationships[0].spdx_element_id,
        RelationshipType.DESCRIBES,
        [],
        creation_info=creation_info,
        comment=relationships[0].comment,
        completeness=RelationshipCompleteness.NOASSERTION,
    )
    assert payload.get_element(f"{document_namespace}#SPDXRef-Relationship-1") == Relationship(
        f"{document_namespace}#SPDXRef-Relationship-1",
        relationships[1].spdx_element_id,
        RelationshipType.DESCRIBES,
        [relationships[1].related_spdx_element_id],
        creation_info=creation_info,
        comment=relationships[1].comment,
    )
    assert payload.get_element(f"{document_namespace}#SPDXRef-Relationship-2") == Relationship(
        f"{document_namespace}#SPDXRef-Relationship-2",
        relationships[2].spdx_element_id,
        RelationshipType.SPECIFICATION_FOR,
        [],
        creation_info=creation_info,
        completeness=RelationshipCompleteness.COMPLETE,
    )


@mock.patch("spdx_tools.spdx3.model.CreationInfo", autospec=True)
def test_undefined_relationship_bump(creation_info, capsys):
    relationships = [
        relationship_fixture(
            related_spdx_element_id=SpdxNoAssertion(), relationship_type=Spdx2_RelationshipType.CONTAINED_BY
        ),
        relationship_fixture(relationship_type=Spdx2_RelationshipType.OPTIONAL_COMPONENT_OF),
    ]
    payload = Payload()
    document_namespace = "https://doc.namespace"
    bump_relationships(relationships, payload, creation_info, document_namespace)

    captured = capsys.readouterr()
    assert (
        captured.err == "Swapped Relationship to NoAssertion/None not converted: missing conversion rule \n"
        "OPTIONAL_COMPONENT_OF not converted: missing conversion rule \n"
    )
