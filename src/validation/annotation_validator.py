from typing import List

from src.model.annotation import Annotation
from src.validation.validation_message import ValidationMessage


class AnnotationValidator:
    spdx_version: str

    def __init__(self, spdx_version):
        self.spdx_version = spdx_version

    def validate_annotations(self, annotations: List[Annotation]) -> List[ValidationMessage]:
        error_messages = []
        for annotation in annotations:
            error_messages.extend(self.validate_annotation(annotation))

        return error_messages

    def validate_annotation(self, annotation: Annotation) -> List[ValidationMessage]:
        pass
