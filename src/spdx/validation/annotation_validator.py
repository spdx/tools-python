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

from spdx.model.annotation import Annotation
from spdx.model.document import Document
from spdx.validation.actor_validator import validate_actor
from spdx.validation.spdx_id_validators import validate_spdx_id
from spdx.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


def validate_annotations(annotations: List[Annotation], document: Document) -> List[ValidationMessage]:
    validation_messages = []
    for annotation in annotations:
        validation_messages.extend(validate_annotation(annotation, document))

    return validation_messages


def validate_annotation(annotation: Annotation, document: Document) -> List[ValidationMessage]:
    validation_messages = []
    context = ValidationContext(element_type=SpdxElementType.ANNOTATION,
                                full_element=annotation)

    validation_messages.extend(validate_actor(annotation.annotator, "annotation"))

    messages: List[str] = validate_spdx_id(annotation.spdx_id, document, check_document=True)
    for message in messages:
        validation_messages.append(ValidationMessage(message, context))

    return validation_messages
