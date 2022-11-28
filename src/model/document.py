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
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from typeguard import typechecked

from src.model.actor import Actor
from src.model.annotation import Annotation
from src.model.external_document_ref import ExternalDocumentRef
from src.model.extracted_licensing_info import ExtractedLicensingInfo
from src.model.file import File
from src.model.package import Package
from src.model.relationship import Relationship
from src.model.snippet import Snippet
from src.model.dataclass_with_properties import dataclass_with_properties
from src.model.version import Version


@dataclass_with_properties
class CreationInfo:
    creators: List[Actor]
    created: datetime
    comment: Optional[str] = None
    license_list_version: Optional[Version] = None


@dataclass_with_properties
class Document:
    spdx_version: str
    spdx_id: str
    name: str
    document_namespace: str
    creation_info: CreationInfo
    data_license: str = "CC0-1.0"
    external_document_refs: List[ExternalDocumentRef] = field(default_factory=list)
    comment: Optional[str] = None

    packages: List[Package] = field(default_factory=list)
    files: List[File] = field(default_factory=list)
    snippets: List[Snippet] = field(default_factory=list)
    annotations: List[Annotation] = field(default_factory=list)
    relationships: List[Relationship] = field(default_factory=list)
    extracted_licensing_info: List[ExtractedLicensingInfo] = field(default_factory=list)
