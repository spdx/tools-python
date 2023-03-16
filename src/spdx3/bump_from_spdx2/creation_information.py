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
from datetime import datetime
from typing import List

from semantic_version import Version
from spdx3.payload import Payload

from spdx.model.document import CreationInfo as Spdx2_CreationInfo
from spdx3.bump_from_spdx2.actor import bump_actor
from spdx3.bump_from_spdx2.external_document_ref import bump_external_document_ref
from spdx3.bump_from_spdx2.message import print_missing_conversion
from spdx3.model.creation_information import CreationInformation
from spdx3.model.spdx_document import SpdxDocument


def bump_creation_information(spdx2_creation_info: Spdx2_CreationInfo, payload: Payload) -> SpdxDocument:
    # creation_info.spdx_id -> spdx_document.spdx_id
    spdx_id = spdx2_creation_info.spdx_id

    # creation_info.name -> spdx_document.name
    name = spdx2_creation_info.name

    # creation_info.document_namespace -> ?
    print_missing_conversion("creation_info.document_namespace", 0)

    created: datetime = spdx2_creation_info.created
    # creation_info.creator_comment -> ?
    print_missing_conversion("creation_info.creator_comment", 0)
    data_license = spdx2_creation_info.data_license
    # creation_info.external_document_refs -> spdx_document.imports
    imports = [bump_external_document_ref(external_document_ref) for external_document_ref in
               spdx2_creation_info.external_document_refs]
    # creation_info.license_list_version -> ?
    print_missing_conversion("creation_info.license_list_version", 0)
    # creation_info.document_comment -> spdx_document.comment
    document_comment = spdx2_creation_info.document_comment
    creation_information = CreationInformation(Version("3.0.0"), created, [], ["core", "software", "licensing"],
                                               data_license)

    # due to the cyclic dependency of creators having creators themselves,
    # we have to add them to the creation_information after initializing it
    creator_ids: List[str] = []
    for creator in spdx2_creation_info.creators:
        creator_ids.append(bump_actor(creator, payload, creation_information, is_agent=True))
    creation_information.created_by = creator_ids

    spdx_document = SpdxDocument(spdx_id=spdx_id, creation_info=creation_information, name=name,
                                 comment=document_comment, elements=[], root_elements=[], imports=imports)

    return spdx_document
