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
from spdx3.spdx_id_map import SpdxIdMap

""" We want to implement a bump_from_spdx2 from the data model in src.spdx to the data model in src.spdx3.
    As there are many fundamental differences between these version we want each bump_from_spdx2 method to take
    the object from src.spdx and return all objects that the input is translated to."""


def bump_spdx_document(document: Spdx2_Document) -> SpdxIdMap:
    spdx_id_map = SpdxIdMap()
    spdx_document: SpdxDocument = bump_creation_information(document.creation_info)
    creation_info: CreationInformation = spdx_document.creation_info

    spdx_id_map.add_element(spdx_document)

    for spdx2_package in document.packages:
        package = bump_package(spdx2_package, creation_info)
        spdx_id_map.add_element(package)
        spdx_document.elements.append(package.spdx_id)

    for spdx2_file in document.files:
        file = bump_file(spdx2_file, creation_info)
        spdx_id_map.add_element(file)
        spdx_document.elements.append(file.spdx_id)

    for spdx2_snippet in document.snippets:
        snippet = bump_snippet(spdx2_snippet, creation_info)
        spdx_id_map.add_element(snippet)
        spdx_document.elements.append(snippet.spdx_id)

    for counter, spdx2_relationship in enumerate(document.relationships):
        relationship = bump_relationship(spdx2_relationship, creation_info, counter)
        spdx_id_map.add_element(relationship)
        spdx_document.elements.append(relationship.spdx_id)

    for counter, spdx2_annotation in enumerate(document.annotations):
        annotation = bump_annotation(spdx2_annotation, creation_info, counter)
        spdx_id_map.add_element(annotation)
        spdx_document.elements.append(annotation.spdx_id)

    return spdx_id_map
