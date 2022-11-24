from enum import Enum, auto
from typing import Optional, Any


class SpdxElementType(Enum):
    DOCUMENT = auto()
    PACKAGE = auto()
    FILE = auto()
    SNIPPET = auto()
    LICENSE = auto()
    ANNOTATION = auto()
    RELATIONSHIP = auto()
    EXTERNAL_DOCUMENT = auto()
    EXTRACTED_LICENSING_INFO = auto()


class ValidationContext:
    spdx_id: Optional[str]  # not every type has an id, or it might be missing
    parent_id: Optional[str]  # if a parent is known and has a valid id
    element_type: SpdxElementType
    full_element: Any  # can be any class of the data model

    def __init__(self, spdx_id: Optional[str] = None, parent_id: Optional[str] = None, element_type: SpdxElementType = None, full_element: Any = None):
        self.spdx_id = spdx_id
        self.parent_id = parent_id
        self.element_type = element_type
        self.full_element = full_element


class ValidationMessage:
    validation_message: str
    context: ValidationContext

    def __init__(self, validation_message: str, context: ValidationContext):
        self.validation_message = validation_message
        self.context = context
