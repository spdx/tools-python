# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from spdx_tools.spdx3.bump_from_spdx2.relationship import bump_relationship, bump_relationships
from spdx_tools.spdx3.model import Relationship, RelationshipCompleteness, RelationshipType
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx.model import RelationshipType as Spdx2_RelationshipType
from spdx_tools.spdx.model import SpdxNoAssertion, SpdxNone
from tests.spdx.fixtures import relationship_fixture


def test_relationship_bump():
    spdx2_relationship = relationship_fixture()
    document_namespace = "https://doc.namespace"
    relationship = bump_relationship(spdx2_relationship, document_namespace, 1)

    assert relationship == Relationship(
        f"{document_namespace}#SPDXRef-Relationship-1",
        f"{document_namespace}#{spdx2_relationship.spdx_element_id}",
        RelationshipType.DESCRIBES,
        [f"{document_namespace}#{spdx2_relationship.related_spdx_element_id}"],
        comment=spdx2_relationship.comment,
    )


def test_relationships_bump():
    relationships = [
        relationship_fixture(comment=None),
        relationship_fixture(related_spdx_element_id="SPDXRef-Package", comment=None),
    ]
    payload = Payload()
    document_namespace = "https://doc.namespace"
    bump_relationships(relationships, payload, document_namespace)

    assert payload.get_element(f"{document_namespace}#SPDXRef-Relationship-1") == Relationship(
        f"{document_namespace}#SPDXRef-Relationship-1",
        f"{document_namespace}#{relationships[0].spdx_element_id}",
        RelationshipType.DESCRIBES,
        [
            f"{document_namespace}#{relationships[0].related_spdx_element_id}",
            f"{document_namespace}#{relationships[1].related_spdx_element_id}",
        ],
    )


def test_relationships_bump_with_setting_completeness():
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
    bump_relationships(relationships, payload, document_namespace)

    assert payload.get_element(f"{document_namespace}#SPDXRef-Relationship-0") == Relationship(
        f"{document_namespace}#SPDXRef-Relationship-0",
        f"{document_namespace}#{relationships[0].spdx_element_id}",
        RelationshipType.DESCRIBES,
        [],
        comment=relationships[0].comment,
        completeness=RelationshipCompleteness.NOASSERTION,
    )
    assert payload.get_element(f"{document_namespace}#SPDXRef-Relationship-1") == Relationship(
        f"{document_namespace}#SPDXRef-Relationship-1",
        f"{document_namespace}#{relationships[1].spdx_element_id}",
        RelationshipType.DESCRIBES,
        [f"{document_namespace}#{relationships[1].related_spdx_element_id}"],
        comment=relationships[1].comment,
    )
    assert payload.get_element(f"{document_namespace}#SPDXRef-Relationship-2") == Relationship(
        f"{document_namespace}#SPDXRef-Relationship-2",
        f"{document_namespace}#{relationships[2].spdx_element_id}",
        RelationshipType.SPECIFICATION_FOR,
        [],
        completeness=RelationshipCompleteness.COMPLETE,
    )


def test_undefined_relationship_bump(capsys):
    relationships = [
        relationship_fixture(
            related_spdx_element_id=SpdxNoAssertion(), relationship_type=Spdx2_RelationshipType.CONTAINED_BY
        ),
        relationship_fixture(relationship_type=Spdx2_RelationshipType.OPTIONAL_COMPONENT_OF),
    ]
    payload = Payload()
    document_namespace = "https://doc.namespace"
    bump_relationships(relationships, payload, document_namespace)

    captured = capsys.readouterr()
    assert (
        captured.err == "Swapped Relationship to NoAssertion/None not converted: missing conversion rule \n"
        "OPTIONAL_COMPONENT_OF not converted: missing conversion rule \n"
    )
