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
from semantic_version import Version

from spdx.model.document import Document as Spdx2_Document
from spdx3.model.spdx_document import SpdxDocument

from spdx3.bump_from_spdx2.spdx_document import bump_spdx_document
from tests.fixtures import document_fixture


def test_bump_spdx_document():
    spdx2_document: Spdx2_Document = document_fixture()

    spdx_document: SpdxDocument = bump_spdx_document(spdx2_document)

    assert spdx_document.spdx_id == "SPDXRef-DOCUMENT"
    assert spdx_document.name == "documentName"
    assert spdx_document.creation_info.spec_version == Version("3.0.0")
    assert len(spdx_document.elements) == 3 # document_fixture has exactly one package, one file and one snippet which are added to the elements list during bump_from_spdx2
