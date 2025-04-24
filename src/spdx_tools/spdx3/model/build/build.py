# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from dataclasses import field
from datetime import datetime

from beartype.typing import Dict, List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values

from ..core.creation_info import CreationInfo
from ..core.element import Element
from ..core.external_identifier import ExternalIdentifier
from ..core.external_ref import ExternalRef
from ..core.hash import Hash
from ..core.integrity_method import IntegrityMethod


@dataclass_with_properties
class Build(Element):
    build_type: str = ""
    build_id: Optional[str] = None
    config_source_entrypoint: List[str] = field(default_factory=list)
    config_source_uri: List[str] = field(default_factory=list)
    config_source_digest: List[Hash] = field(default_factory=list)
    parameter: Dict[str, str] = field(default_factory=dict)
    build_start_time: Optional[datetime] = None
    build_end_time: Optional[datetime] = None
    environment: Dict[str, str] = field(default_factory=dict)

    def __init__(
        self,
        spdx_id: str,
        build_type: str,
        creation_info: Optional[CreationInfo] = None,
        name: Optional[str] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        comment: Optional[str] = None,
        verified_using: List[IntegrityMethod] = [],
        external_ref: List[ExternalRef] = [],
        external_identifier: List[ExternalIdentifier] = [],
        extension: Optional[str] = None,
        build_id: Optional[str] = None,
        config_source_entrypoint: List[str] = [],
        config_source_uri: List[str] = [],
        config_source_digest: List[Hash] = [],
        parameter: Dict[str, str] = {},
        build_start_time: Optional[datetime] = None,
        build_end_time: Optional[datetime] = None,
        environment: Dict[str, str] = {},
    ):
        verified_using = [] if not verified_using else verified_using
        external_ref = [] if not external_ref else external_ref
        external_identifier = [] if not external_identifier else external_identifier
        config_source_entrypoint = [] if not config_source_entrypoint else config_source_entrypoint
        config_source_uri = [] if not config_source_uri else config_source_uri
        config_source_digest = [] if not config_source_digest else config_source_digest
        parameter = {} if not parameter else parameter
        environment = {} if not environment else environment

        check_types_and_set_values(self, locals())
