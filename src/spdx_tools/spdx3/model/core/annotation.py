# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from dataclasses import field
from enum import Enum, auto

from beartype.typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model.core import CreationInfo, Element, ExternalIdentifier, ExternalRef, IntegrityMethod


class AnnotationType(Enum):
    REVIEW = auto()
    OTHER = auto()


@dataclass_with_properties
class Annotation(Element):
    annotation_type: AnnotationType = None
    subject: str = None
    content_type: List[str] = field(default_factory=list)  # placeholder for MediaType
    statement: Optional[str] = None

    def __init__(
        self,
        spdx_id: str,
        annotation_type: AnnotationType,
        subject: str,
        creation_info: Optional[CreationInfo] = None,
        name: Optional[str] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        comment: Optional[str] = None,
        verified_using: List[IntegrityMethod] = [],
        external_ref: List[ExternalRef] = [],
        external_identifier: List[ExternalIdentifier] = [],
        extension: Optional[str] = None,
        content_type: List[str] = [],
        statement: Optional[str] = None,
    ):
        verified_using = [] if not verified_using else verified_using
        external_ref = [] if not external_ref else external_ref
        external_identifier = [] if not external_identifier else external_identifier
        content_type = [] if not content_type else content_type
        check_types_and_set_values(self, locals())
