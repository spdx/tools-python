from typing import List

from src.model.external_document_ref import ExternalDocumentRef
from src.validation.validation_message import ValidationMessage


class ExternalDocumentRefValidator:
    spdx_version: str

    def __init__(self, spdx_version):
        self.spdx_version = spdx_version

    def validate_external_document_refs(self, external_document_refs: List[ExternalDocumentRef]) -> List[ValidationMessage]:
        error_messages = []
        for external_document_ref in external_document_refs:
            error_messages.extend(self.validate_external_document_ref(external_document_ref))

        return error_messages

    def validate_external_document_ref(self, external_document_ref: ExternalDocumentRef) -> List[ValidationMessage]:
        pass
