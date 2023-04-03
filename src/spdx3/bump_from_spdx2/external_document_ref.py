# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import List

from spdx3.bump_from_spdx2.checksum import bump_checksum
from spdx3.model.external_map import ExternalMap
from spdx3.model.hash import Hash
from spdx.model.external_document_ref import ExternalDocumentRef


def bump_external_document_ref(external_document_ref: ExternalDocumentRef) -> ExternalMap:
    external_id: str = external_document_ref.document_ref_id
    verified_using: List[Hash] = [bump_checksum(external_document_ref.checksum)]
    location_hint: str = external_document_ref.document_uri

    return ExternalMap(external_id, verified_using, location_hint)
