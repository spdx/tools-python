from typing import List

from src.model.annotation import Annotation
from src.model.document import Document
from src.validation.actor_validator import ActorValidator
from src.validation.spdx_id_validator import validate_spdx_id_reference
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


class AnnotationValidator:
    spdx_version: str
    document: Document
    actor_validator: ActorValidator

    def __init__(self, spdx_version: str, document: Document):
        self.spdx_version = spdx_version
        self.document = document
        self.actor_validator = ActorValidator(spdx_version)

    def validate_annotations(self, annotations: List[Annotation]) -> List[ValidationMessage]:
        validation_messages = []
        for annotation in annotations:
            validation_messages.extend(self.validate_annotation(annotation))

        return validation_messages

    def validate_annotation(self, annotation: Annotation) -> List[ValidationMessage]:
        validation_messages = []
        document_spdx_id: str = self.document.creation_info.spdx_id
        context = ValidationContext(parent_id=document_spdx_id, element_type=SpdxElementType.ANNOTATION,
                                    full_element=annotation)

        validation_messages.append(
            self.actor_validator.validate_actor(annotation.annotator)
        )

        message: str = validate_spdx_id_reference(annotation.spdx_id, self.document)
        if message:
            validation_messages.append(ValidationMessage(message, context))

        return validation_messages

