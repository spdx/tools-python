import re
from typing import List

from src.model.external_document_ref import ExternalDocumentRef
from src.validation.checksum_validator import ChecksumValidator
from src.validation.uri_validator import is_valid_uri
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


class ExternalDocumentRefValidator:
    spdx_version: str
    parent_id: str
    checksum_validator: ChecksumValidator

    def __init__(self, spdx_version: str, parent_id: str):
        self.spdx_version = spdx_version
        self.parent_id = parent_id
        self.checksum_validator = ChecksumValidator(spdx_version, parent_id)

    def validate_external_document_refs(self, external_document_refs: List[ExternalDocumentRef]) -> List[ValidationMessage]:
        validation_messages = []
        for external_document_ref in external_document_refs:
            validation_messages.extend(self.validate_external_document_ref(external_document_ref))

        return validation_messages

    def validate_external_document_ref(self, external_document_ref: ExternalDocumentRef) -> List[ValidationMessage]:
        validation_messages = []
        context = ValidationContext(parent_id=self.parent_id, element_type=SpdxElementType.EXTERNAL_DOCUMENT_REF,
                                    full_element=external_document_ref)

        if not re.match(r"^DocumentRef-[\da-zA-Z.+-]+$", external_document_ref.document_ref_id):
            validation_messages.append(
                ValidationMessage(
                    f'document_ref_id must only contain letters, numbers, ".", "-" and "+" and must begin with "DocumentRef-", but is: {external_document_ref.document_ref_id}',
                    context
                )
            )

        if not is_valid_uri(external_document_ref.document_uri):
            validation_messages.append(
                ValidationMessage(
                    f'document_uri must be a valid URI specified in RFC-3986, '
                    f'but is: {external_document_ref.document_uri}',
                    context
                )
            )

        validation_messages.extend(
            self.checksum_validator.validate_checksum(external_document_ref.checksum)
        )

        return validation_messages
