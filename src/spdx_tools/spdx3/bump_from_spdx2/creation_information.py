# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime
from typing import List

from semantic_version import Version

from spdx_tools.spdx3.bump_from_spdx2.actor import bump_actor
from spdx_tools.spdx3.bump_from_spdx2.external_document_ref import bump_external_document_ref
from spdx_tools.spdx3.bump_from_spdx2.message import print_missing_conversion
from spdx_tools.spdx3.model.creation_information import CreationInformation
from spdx_tools.spdx3.model.spdx_document import SpdxDocument
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx.model.actor import ActorType
from spdx_tools.spdx.model.document import CreationInfo as Spdx2_CreationInfo


def bump_creation_information(spdx2_creation_info: Spdx2_CreationInfo, payload: Payload) -> SpdxDocument:
    # creation_info.spdx_id -> spdx_document.spdx_id
    document_namespace = spdx2_creation_info.document_namespace
    spdx_id = f"{document_namespace}#{spdx2_creation_info.spdx_id}"

    # creation_info.name -> spdx_document.name
    name = spdx2_creation_info.name

    # creation_info.document_namespace -> ?
    print_missing_conversion("creation_info.document_namespace", 0)

    created: datetime = spdx2_creation_info.created
    comment = spdx2_creation_info.document_comment
    data_license = spdx2_creation_info.data_license
    # creation_info.external_document_refs -> spdx_document.imports
    imports = [
        bump_external_document_ref(external_document_ref)
        for external_document_ref in spdx2_creation_info.external_document_refs
    ]
    # creation_info.license_list_version -> ?
    print_missing_conversion("creation_info.license_list_version", 0)
    # creation_info.document_comment -> spdx_document.comment
    document_comment = spdx2_creation_info.document_comment
    creation_information = CreationInformation(
        Version("3.0.0"), created, [], [], ["core", "software", "licensing"], data_license, comment
    )

    # due to creators having a creation_information themselves which inherits from the document's one,
    # we have to add them after the creation_information has been initialized
    creator_ids: List[str] = []
    tool_ids: List[str] = []
    for creator in spdx2_creation_info.creators:
        bumped_actor_id = bump_actor(creator, payload, creation_information, document_namespace)
        if creator.actor_type in [ActorType.PERSON, ActorType.ORGANIZATION]:
            creator_ids.append(bumped_actor_id)
        else:
            tool_ids.append(bumped_actor_id)

    if not creator_ids:
        raise NotImplementedError(
            "The SPDX2 creation_info does not contain creators of Type Person or Organization."
            " This case leads to an invalid SPDX3 document and is currently not supported."
        )

    creation_information.created_by = creator_ids
    creation_information.created_using = tool_ids

    spdx_document = SpdxDocument(
        spdx_id=spdx_id,
        creation_info=creation_information,
        name=name,
        comment=document_comment,
        elements=[],
        root_elements=[],
        imports=imports,
    )

    return spdx_document
