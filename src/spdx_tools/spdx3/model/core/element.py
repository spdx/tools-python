# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from abc import ABC, abstractmethod
from dataclasses import field

from beartype.typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties

from .creation_info import CreationInfo
from .external_identifier import ExternalIdentifier
from .external_ref import ExternalRef
from .integrity_method import IntegrityMethod


@dataclass_with_properties
class Element(ABC):
    spdx_id: str  # IRI
    creation_info: Optional[CreationInfo] = None
    name: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    comment: Optional[str] = None
    verified_using: List[IntegrityMethod] = field(default_factory=list)
    external_ref: List[ExternalRef] = field(default_factory=list)
    external_identifier: List[ExternalIdentifier] = field(default_factory=list)
    extension: Optional[str] = None  # placeholder for extension

    @abstractmethod
    def __init__(self):
        pass
