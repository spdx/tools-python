# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from beartype.typing import List

from spdx_tools.spdx.constants import DOCUMENT_SPDX_ID
from spdx_tools.spdx.model import CreationInfo
from spdx_tools.spdx.validation.actor_validator import validate_actors
from spdx_tools.spdx.validation.external_document_ref_validator import validate_external_document_refs
from spdx_tools.spdx.validation.uri_validators import validate_uri
from spdx_tools.spdx.validation.validation_message import SpdxElementType, ValidationContext, ValidationMessage


def validate_creation_info(creation_info: CreationInfo, spdx_version: str) -> List[ValidationMessage]:
    validation_messages: List[ValidationMessage] = []

    context = ValidationContext(spdx_id=creation_info.spdx_id, element_type=SpdxElementType.DOCUMENT)

    if creation_info.spdx_id != DOCUMENT_SPDX_ID:
        validation_messages.append(
            ValidationMessage(f"spdx_id must be {DOCUMENT_SPDX_ID}, but is: {creation_info.spdx_id}", context)
        )

    if creation_info.data_license != "CC0-1.0":
        validation_messages.append(
            ValidationMessage(f'data_license must be "CC0-1.0", but is: {creation_info.data_license}', context)
        )

    for message in validate_uri(creation_info.document_namespace):
        validation_messages.append(ValidationMessage("document_namespace " + message, context))

    validation_messages.extend(validate_actors(creation_info.creators, creation_info.spdx_id))
    validation_messages.extend(
        validate_external_document_refs(creation_info.external_document_refs, creation_info.spdx_id, spdx_version)
    )

    return validation_messages
