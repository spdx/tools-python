import re
from typing import List

from src.model.document import CreationInfo
from src.validation.actor_validator import ActorValidator
from src.validation.external_document_ref_validator import ExternalDocumentRefValidator
from src.validation.uri_validators import validate_uri
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


class CreationInfoValidator:
    spdx_version: str

    def __init__(self, spdx_version):
        self.spdx_version = spdx_version

    def validate_creation_info(self, creation_info: CreationInfo) -> List[ValidationMessage]:
        validation_messages: List[ValidationMessage] = []
        actor_validator = ActorValidator(self.spdx_version, creation_info.spdx_id)
        external_document_ref_validator = ExternalDocumentRefValidator(self.spdx_version, creation_info.spdx_id)

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

        for message in validate_uri(creation_info.document_namespace):
            validation_messages.append(
                ValidationMessage(
                    'document_namespace ' + message, context
                )
            )

        validation_messages.extend(
            actor_validator.validate_actors(creation_info.creators)
        )

        validation_messages.extend(
            external_document_ref_validator.validate_external_document_refs(creation_info.external_document_refs))

        return validation_messages
