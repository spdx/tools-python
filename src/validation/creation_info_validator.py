import re
from typing import List

from src.model.document import CreationInfo
from src.validation.actor_validator import ActorValidator
from src.validation.uri_validator import is_valid_uri
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


class CreationInfoValidator:
    spdx_version: str
    actor_validator: ActorValidator

    def __init__(self, spdx_version):
        self.spdx_version = spdx_version
        # TODO: make this local to the validate_creation_info method, because we don't know the parent id yet
        self.actor_validator = ActorValidator(spdx_version)

    def validate_creation_info(self, creation_info: CreationInfo) -> List[ValidationMessage]:
        validation_messages: List[ValidationMessage] = []
        context = ValidationContext(spdx_id=creation_info.spdx_id, element_type=SpdxElementType.DOCUMENT)

        if not re.match(r"^SPDX-\d+.\d+$", creation_info.spdx_version):
            validation_messages.append(
                ValidationMessage(
                    f'spdx_version must be of the form "SPDX-[major].[minor]" but is: {creation_info.spdx_version}',
                    context
                )
            )

        if creation_info.spdx_id != "SPDXRef-DOCUMENT":
            validation_messages.append(
                ValidationMessage(
                    f'spdx_id must be SPDXRef-DOCUMENT, but is: {creation_info.spdx_id}',
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

        if not is_valid_uri(creation_info.document_namespace):
            validation_messages.append(
                ValidationMessage(
                    f'document_namespace must be a valid URI specified in RFC-3986, '
                    f'but is: {creation_info.document_namespace}',
                    context
                )
            )

        validation_messages.extend(
            self.actor_validator.validate_actors(creation_info.creators)
        )

        return validation_messages
