#  Copyright (c) 2022 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from datetime import datetime

from src.model.actor import Actor, ActorType
from src.model.document import CreationInfo
from src.model.version import Version

"""Utility methods to create data model instances. All properties have valid defaults, so they don't need to be 
specified unless relevant for the test."""


def creation_info_fixture(spdx_version="spdxVersion", spdx_id="documentId", name="documentName",
                          namespace="documentNamespace", creators=None, created=datetime(2022, 12, 1),
                          creator_comment="creatorComment", data_license="CC0-1.0", external_document_refs=None,
                          license_list_version=Version(3, 19), document_comment="documentComment") -> CreationInfo:
    creators = [Actor(ActorType.PERSON, "creatorName")] if creators is None else creators
    external_document_refs = [] if external_document_refs is None else external_document_refs
    return CreationInfo(spdx_version, spdx_id, name, namespace, creators, created, creator_comment, data_license,
                        external_document_refs, license_list_version, document_comment)
