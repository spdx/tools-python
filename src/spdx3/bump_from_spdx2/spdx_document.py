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

from spdx3.bump_from_spdx2.creation_information import bump_creation_information
from spdx3.bump_from_spdx2.file import bump_file
from spdx3.bump_from_spdx2.package import bump_package
from spdx3.bump_from_spdx2.snippet import bump_snippet
from spdx3.model.spdx_document import SpdxDocument

from spdx.model.document import Document as Spdx2_Document

""" We want to implement a bump_from_spdx2 from the data model in src.spdx to the data model in src.spdx3.
    As there are many fundamental differences between these version we want each bump_from_spdx2 method to take
    the object from src.spdx and return all objects that the input is translated to."""
def bump_spdx_document(document: Spdx2_Document) -> SpdxDocument:
    spdx_document: SpdxDocument = bump_creation_information(document.creation_info)
    for package in document.packages:
        spdx_document.elements.append(bump_package(package, creation_information=spdx_document.creation_info))

    for file in document.files:
        spdx_document.elements.append(bump_file(file, creation_information=spdx_document.creation_info))

    for snippet in document.snippets:
        spdx_document.elements.append(bump_snippet(snippet, creation_information=spdx_document.creation_info))

    return spdx_document

