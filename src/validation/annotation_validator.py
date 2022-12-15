from typing import List

from src.model.annotation import Annotation
from src.model.document import Document
from src.validation.actor_validator import ActorValidator
from src.validation.spdx_id_validation import validate_spdx_id
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


class AnnotationValidator:
    spdx_version: str
    document: Document
    actor_validator: ActorValidator

    def __init__(self, spdx_version: str, document: Document):
        self.spdx_version = spdx_version
        self.document = document
        self.actor_validator = ActorValidator(spdx_version, parent_id=None)

    def validate_annotations(self, annotations: List[Annotation]) -> List[ValidationMessage]:
        validation_messages = []
        for annotation in annotations:
            validation_messages.extend(self.validate_annotation(annotation))

        return validation_messages

    def validate_annotation(self, annotation: Annotation) -> List[ValidationMessage]:
        validation_messages = []
        context = ValidationContext(element_type=SpdxElementType.ANNOTATION,
                                    full_element=annotation)

        validation_messages.extend(self.actor_validator.validate_actor(annotation.annotator))

        messages: List[str] = validate_spdx_id(annotation.spdx_id, self.document, check_document=True)
        for message in messages:
            validation_messages.append(ValidationMessage(message, context))

        return validation_messages
