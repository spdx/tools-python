from enum import Enum, auto

from beartype.typing import Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model import IntegrityMethod


class ContentIdentifierType(Enum):
    GITOID = auto()
    SWHID = auto()


@dataclass_with_properties
class ContentIdentifier(IntegrityMethod):
    content_identifier_type: ContentIdentifierType = None
    content_identifier_value: str = None

    def __init__(
        self,
        content_identifier_type: ContentIdentifierType,
        content_identifier_value: str,
        comment: Optional[str] = None,
    ):
        check_types_and_set_values(self, locals())
