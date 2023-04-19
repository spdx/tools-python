# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime
from enum import Enum, auto

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx.model import Actor


class AnnotationType(Enum):
    REVIEW = auto()
    OTHER = auto()


@dataclass_with_properties
class Annotation:
    spdx_id: str
    annotation_type: AnnotationType
    annotator: Actor
    annotation_date: datetime
    annotation_comment: str

    def __init__(
        self,
        spdx_id: str,
        annotation_type: AnnotationType,
        annotator: Actor,
        annotation_date: datetime,
        annotation_comment: str,
    ):
        check_types_and_set_values(self, locals())
