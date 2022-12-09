from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Any


class SpdxElementType(Enum):
    CHECKSUM = auto()
    EXTERNAL_PACKAGE_REF = auto()
    ACTOR = auto()
    DOCUMENT = auto()
    CREATION_INFO = auto()
    PACKAGE = auto()
    FILE = auto()
    SNIPPET = auto()
    LICENSE = auto()
    ANNOTATION = auto()
    RELATIONSHIP = auto()
    EXTERNAL_DOCUMENT = auto()
    EXTRACTED_LICENSING_INFO = auto()


@dataclass(eq=True, frozen=True)
class ValidationContext:
    spdx_id: Optional[str] = None  # not every type has an id, or it might be missing
    parent_id: Optional[str] = None  # if a parent is known and has a valid id
    element_type: Optional[SpdxElementType] = None
    full_element: Any = None  # can be any class of the data model


@dataclass(eq=True, frozen=True)
class ValidationMessage:
    validation_message: str
    context: ValidationContext
