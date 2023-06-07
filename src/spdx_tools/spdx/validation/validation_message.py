# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass
from enum import Enum, auto

from beartype.typing import Any, Optional


class SpdxElementType(Enum):
    LICENSE_EXPRESSION = auto()
    PACKAGE_VERIFICATION_CODE = auto()
    EXTERNAL_DOCUMENT_REF = auto()
    CHECKSUM = auto()
    EXTERNAL_PACKAGE_REF = auto()
    ACTOR = auto()
    DOCUMENT = auto()
    CREATION_INFO = auto()
    PACKAGE = auto()
    FILE = auto()
    SNIPPET = auto()
    ANNOTATION = auto()
    RELATIONSHIP = auto()
    EXTRACTED_LICENSING_INFO = auto()


@dataclass(frozen=True)
class ValidationContext:
    spdx_id: Optional[str] = None  # not every type has an id, or it might be missing
    parent_id: Optional[str] = None  # if a parent is known and has a valid id
    element_type: Optional[SpdxElementType] = None
    full_element: Any = None  # can be any class of the data model


@dataclass(frozen=True)
class ValidationMessage:
    validation_message: str
    context: ValidationContext
