# Copyright (c) 2022 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from datetime import datetime
from typing import List, Optional

from src.model.actor import Actor
from src.model.annotation import Annotation
from src.model.external_document_ref import ExternalDocumentRef
from src.model.extracted_licensing_info import ExtractedLicensingInfo
from src.model.file import File
from src.model.package import Package
from src.model.relationship import Relationship
from src.model.snippet import Snippet
from src.model.version import Version


class CreationInfo:
    creators: List[Actor]
    created: datetime
    comment: Optional[str]
    license_list_version: Optional[Version]

    def __init__(self, creators: List[Actor], created: datetime, comment: Optional[str] = None,
                 license_list_version: Optional[Version] = None):
        self.creators = creators
        self.created = created
        self.comment = comment
        self.license_list_version = license_list_version


class Document:
    data_license = "CC0-1.0"
    spdx_version: str
    spdx_id: str
    name: str
    document_namespace: str
    creation_info: CreationInfo
    external_document_refs: List[ExternalDocumentRef]
    comment: Optional[str]

    packages: List[Package]
    files: List[File]
    snippets: List[Snippet]
    annotations: List[Annotation]
    relationships: List[Relationship]
    extracted_licensing_info: List[ExtractedLicensingInfo]

    def __init__(self, spdx_version: str, spdx_id: str, name: str, document_namespace: str,
                 creation_info: CreationInfo, external_document_refs: List[ExternalDocumentRef] = None,
                 comment: Optional[str] = None, packages: List[Package] = None, files: List[File] = None,
                 snippets: List[Snippet] = None, annotations: List[Annotation] = None,
                 relationships: List[Relationship] = None,
                 extracted_licensing_info: List[ExtractedLicensingInfo] = None):
        self.spdx_version = spdx_version
        self.spdx_id = spdx_id
        self.name = name
        self.document_namespace = document_namespace
        self.creation_info = creation_info
        self.external_document_refs = external_document_refs or []
        self.comment = comment
        self.packages = packages or []
        self.files = files or []
        self.snippets = snippets or []
        self.annotations = annotations or []
        self.relationships = relationships or []
        self.extracted_licensing_info = extracted_licensing_info or []
