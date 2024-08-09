# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from beartype.typing import List, Set

from spdx_tools.spdx.model import Annotation, Document
from spdx_tools.spdx.validation.actor_validator import validate_actor
from spdx_tools.spdx.validation.spdx_id_validators import validate_spdx_id, get_all_spdx_ids
from spdx_tools.spdx.validation.validation_message import SpdxElementType, ValidationContext, ValidationMessage


def validate_annotations(annotations: List[Annotation], document: Document) -> List[ValidationMessage]:
    validation_messages = []

    all_spdx_ids: Set[str] = get_all_spdx_ids(document)

    for annotation in annotations:
        validation_messages.extend(validate_annotation(annotation, document, all_spdx_ids))

    return validation_messages


def validate_annotation(annotation: Annotation, document: Document, all_spdx_ids: Set[str]) -> List[ValidationMessage]:
    validation_messages = []
    context = ValidationContext(element_type=SpdxElementType.ANNOTATION, full_element=annotation)

    validation_messages.extend(validate_actor(annotation.annotator, "annotation"))

    messages: List[str] = validate_spdx_id(annotation.spdx_id, document, all_spdx_ids, check_document=True)
    for message in messages:
        validation_messages.append(ValidationMessage(message, context))

    return validation_messages
