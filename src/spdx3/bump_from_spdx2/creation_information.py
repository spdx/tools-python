#  Copyright (c) 2023 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from datetime import datetime

from semantic_version import Version

from spdx3.bump_from_spdx2.message import print_missing_conversion
from spdx3.model.spdx_document import SpdxDocument

from spdx3.model.creation_information import CreationInformation

from spdx.model.document import CreationInfo as Spdx2_CreationInfo


def bump_creation_information(spdx2_creation_info: Spdx2_CreationInfo) -> SpdxDocument:
    # creation_info.spdx_id -> spdx_document.spdx_id
    spdx_id = spdx2_creation_info.spdx_id

    # creation_info.name -> spdx_document.name
    name = spdx2_creation_info.name

    # creation_info.document_namespace -> ?
    print("\n")
    print_missing_conversion("creation_info.document_namespace", 0)
    # creation_info.creators -> creation_information.creators (not implemented yet)
    print_missing_conversion("creation_info.creators", 1, "of creators")
    created: datetime = spdx2_creation_info.created
    # creation_info.creator_comment -> ?
    print_missing_conversion("creation_info.creator_comment", 0)
    data_license = spdx2_creation_info.data_license
    # creation_info.external_document_refs -> spdx_document.imports
    imports = spdx2_creation_info.external_document_refs
    print_missing_conversion("creation_info.external_document_refs", 0, "ExternalDocumentRef -> ExternalMap")
    # creation_info.license_list_version -> ?
    print_missing_conversion("creation_info.license_list_version", 0)
    # creation_info.document_comment -> spdx_document.comment
    document_comment = spdx2_creation_info.document_comment
    creation_information = CreationInformation(Version("3.0.0"), created, None, ["core", "software", "licensing"], data_license)
    spdx_document = SpdxDocument(spdx_id=spdx_id, creation_info=creation_information, name=name,
                                 comment=document_comment, elements=[], root_elements=[])

    return spdx_document
