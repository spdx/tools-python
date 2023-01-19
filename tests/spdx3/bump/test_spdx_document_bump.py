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
from spdx3.spdx_id_map import SpdxIdMap
from spdx3.writer.console.spdx_id_map_writer import write_spdx_id_map
from tests.spdx.fixtures import document_fixture


def test_bump_spdx_document():
    spdx2_document: Spdx2_Document = document_fixture()

    spdx_id_map: SpdxIdMap = bump_spdx_document(spdx2_document)

    write_spdx_id_map(spdx_id_map, sys.stdout)

    assert "SPDXRef-Package" in list(spdx_id_map.get_full_map().keys())
    assert len(
        spdx_id_map.get_full_map().values()) == 6
