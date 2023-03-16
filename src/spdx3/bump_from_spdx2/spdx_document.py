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
from spdx.model.document import Document as Spdx2_Document
from spdx3.bump_from_spdx2.annotation import bump_annotation
from spdx3.bump_from_spdx2.creation_information import bump_creation_information
from spdx3.bump_from_spdx2.file import bump_file
from spdx3.bump_from_spdx2.package import bump_package
from spdx3.bump_from_spdx2.relationship import bump_relationship
from spdx3.bump_from_spdx2.snippet import bump_snippet
from spdx3.model.creation_information import CreationInformation
from spdx3.model.spdx_document import SpdxDocument
from spdx3.payload import Payload

""" We want to implement a bump_from_spdx2 from the data model in src.spdx to the data model in src.spdx3.
    As there are many fundamental differences between these version we want each bump_from_spdx2 method to take
    the object from src.spdx and add all objects that the input is translated to into the payload."""


def bump_spdx_document(document: Spdx2_Document) -> Payload:
    payload = Payload()
    spdx_document: SpdxDocument = bump_creation_information(document.creation_info, payload)
    creation_info: CreationInformation = spdx_document.creation_info

    payload.add_element(spdx_document)

    for spdx2_package in document.packages:
        bump_package(spdx2_package, payload, creation_info)

    for spdx2_file in document.files:
        bump_file(spdx2_file, payload, creation_info)

    for spdx2_snippet in document.snippets:
        bump_snippet(spdx2_snippet, payload, creation_info)

    for counter, spdx2_relationship in enumerate(document.relationships):
        bump_relationship(spdx2_relationship, payload, creation_info, counter)

    for counter, spdx2_annotation in enumerate(document.annotations):
        bump_annotation(spdx2_annotation, payload, creation_info, counter)

    spdx_document.elements = [spdx_id for spdx_id in payload.get_full_map() if spdx_id != spdx_document.spdx_id]

    return payload
