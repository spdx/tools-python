import re
from typing import List

from src.model.document import CreationInfo
from src.validation.actor_validator import ActorValidator
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


class CreationInfoValidator:
    spdx_version: str
    actor_validator: ActorValidator

    def __init__(self, spdx_version):
        self.spdx_version = spdx_version
        self.actor_validator = ActorValidator(spdx_version)

    def validate_creation_info(self, creation_info: CreationInfo) -> List[ValidationMessage]:
        validation_messages: List[ValidationMessage] = []

        if not re.match(r"SPDX-[0-9]+.[0-9]+", creation_info.spdx_version):
            validation_messages.append(
                ValidationMessage(
                    'spdx_version must be of the form "SPDX-[major].[minor]" but is: ' + creation_info.spdx_version,
                    ValidationContext(spdx_id=creation_info.spdx_id, element_type=SpdxElementType.DOCUMENT))
            )

        if creation_info.spdx_id != "SPDXRef-DOCUMENT":
            validation_messages.append(
                ValidationMessage(
                    'spdx_id must be SPDXRef-DOCUMENT, but is: ' + creation_info.spdx_id,
                    ValidationContext(spdx_id=creation_info.spdx_id, element_type=SpdxElementType.DOCUMENT))
            )

        if creation_info.data_license != "CC0-1.0":
            validation_messages.append(
                ValidationMessage(
                    'data_license must be "CC0-1.0", but is: ' + creation_info.data_license,
                    ValidationContext(spdx_id=creation_info.spdx_id, element_type=SpdxElementType.DOCUMENT))
            )



        validation_messages.extend(
            self.actor_validator.validate_actors(creation_info.creators)
        )

        return validation_messages
