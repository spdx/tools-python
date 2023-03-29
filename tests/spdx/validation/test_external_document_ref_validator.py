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

from typing import List

from spdx.validation.external_document_ref_validator import validate_external_document_ref
from spdx.validation.validation_message import ValidationMessage
from tests.spdx.fixtures import external_document_ref_fixture


def test_valid_external_document_ref():
    external_document_ref = external_document_ref_fixture()
    validation_messages: List[ValidationMessage] = validate_external_document_ref(external_document_ref, "parent_id",
                                                                                  "SPDX-2.3")

    assert validation_messages == []
