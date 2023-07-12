# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import List
from semantic_version import Version

from spdx_tools.spdx3.bump_from_spdx2.actor import bump_actor
from spdx_tools.spdx3.bump_from_spdx2.external_document_ref import bump_external_document_ref
from spdx_tools.spdx3.bump_from_spdx2.message import print_missing_conversion
from spdx_tools.spdx3.model import CreationInfo, ProfileIdentifierType, SpdxDocument
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx.model.actor import ActorType
from spdx_tools.spdx.model.document import CreationInfo as Spdx2_CreationInfo


def bump_creation_info(spdx2_creation_info: Spdx2_CreationInfo, payload: Payload) -> SpdxDocument:
    document_namespace = spdx2_creation_info.document_namespace
    spdx_id = f"{document_namespace}#{spdx2_creation_info.spdx_id}"

    print_missing_conversion("creation_info.document_namespace", 0, "https://github.com/spdx/spdx-3-model/issues/87")

    namespaces, imports = (
        zip(
            *[
                bump_external_document_ref(external_document_ref)
                for external_document_ref in spdx2_creation_info.external_document_refs
            ]
        )
        if spdx2_creation_info.external_document_refs
        else ([], [])
    )
    namespaces = list(namespaces)
    imports = list(imports)
    print_missing_conversion(
        "creation_info.license_list_version",
        0,
        "part of licensing profile, " "https://github.com/spdx/spdx-3-model/issues/131",
    )
    creation_info = CreationInfo(
        spec_version=Version("3.0.0"),
        created=spdx2_creation_info.created,
        created_by=[],
        profile=[ProfileIdentifierType.CORE, ProfileIdentifierType.SOFTWARE, ProfileIdentifierType.LICENSING],
        data_license="https://spdx.org/licenses/" + spdx2_creation_info.data_license,
    )

    # due to creators having a creation_info themselves which inherits from the document's one,
    # we have to add them after the creation_info has been initialized
    creator_ids: List[str] = []
    tool_ids: List[str] = []
    for creator in spdx2_creation_info.creators:
        bumped_actor_id = bump_actor(creator, payload, document_namespace, creation_info)
        if creator.actor_type in [ActorType.PERSON, ActorType.ORGANIZATION]:
            creator_ids.append(bumped_actor_id)
        else:
            tool_ids.append(bumped_actor_id)

    if not creator_ids:
        print_missing_conversion(
            "Creators",
            0,
            "The SPDX2 creation_info does not contain creators of Type Person or Organization."
            " This case leads to an invalid SPDX3 document and is currently not supported."
            "https://github.com/spdx/spdx-3-model/issues/180",
        )

    creation_info.created_by = creator_ids
    creation_info.created_using = tool_ids

    return SpdxDocument(
        spdx_id=spdx_id,
        creation_info=creation_info,
        name=spdx2_creation_info.name,
        comment=spdx2_creation_info.document_comment,
        element=[],
        root_element=[],
        imports=imports,
        namespaces=namespaces,
    )
