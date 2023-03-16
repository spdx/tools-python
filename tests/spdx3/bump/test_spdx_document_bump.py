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
import sys

from spdx.model.document import Document as Spdx2_Document
from spdx3.bump_from_spdx2.spdx_document import bump_spdx_document
from spdx3.payload import Payload
from spdx3.writer.console.payload_writer import write_payload
from tests.spdx.fixtures import document_fixture, creation_info_fixture, annotation_fixture


def test_bump_spdx_document():
    spdx2_document: Spdx2_Document = document_fixture()

    payload: Payload = bump_spdx_document(spdx2_document)

    write_payload(payload, sys.stdout)

    assert "SPDXRef-Package" in payload.get_full_map()
    assert len(payload.get_full_map()) == 9

    # this is more of a temporary test to make sure the dates don't get messed up again
    assert payload.get_element("SPDXRef-DOCUMENT").creation_info.created == creation_info_fixture().created
    assert payload.get_element("SPDXRef-Annotation-0").creation_info.created == annotation_fixture().annotation_date
