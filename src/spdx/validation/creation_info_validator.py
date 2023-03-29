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

from spdx.model.document import CreationInfo
from spdx.validation.actor_validator import validate_actors
from spdx.validation.external_document_ref_validator import validate_external_document_refs
from spdx.validation.uri_validators import validate_uri
from spdx.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


def validate_creation_info(creation_info: CreationInfo, spdx_version: str) -> List[ValidationMessage]:
    validation_messages: List[ValidationMessage] = []

    context = ValidationContext(spdx_id=creation_info.spdx_id, element_type=SpdxElementType.DOCUMENT)

    if creation_info.spdx_id != "SPDXRef-DOCUMENT":
        validation_messages.append(
            ValidationMessage(
                f'spdx_id must be "SPDXRef-DOCUMENT", but is: {creation_info.spdx_id}',
                context
            )
        )

    if creation_info.data_license != "CC0-1.0":
        validation_messages.append(
            ValidationMessage(
                f'data_license must be "CC0-1.0", but is: {creation_info.data_license}',
                context
            )
        )

    for message in validate_uri(creation_info.document_namespace):
        validation_messages.append(
            ValidationMessage(
                "document_namespace " + message, context
            )
        )

    validation_messages.extend(validate_actors(creation_info.creators, creation_info.spdx_id))
    validation_messages.extend(
        validate_external_document_refs(creation_info.external_document_refs, creation_info.spdx_id, spdx_version))

    return validation_messages
