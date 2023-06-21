# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from dataclasses import field
from datetime import datetime

from beartype.typing import Dict, List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model import CreationInfo, Element, ExternalIdentifier, ExternalReference, Hash, IntegrityMethod


@dataclass_with_properties
class Build(Element):
    build_type: str = None
    build_id: Optional[str] = None
    config_source_entrypoint: List[str] = field(default_factory=list)
    config_source_uri: List[str] = field(default_factory=list)
    config_source_digest: List[Hash] = field(default_factory=list)
    parameters: Dict[str, str] = field(default_factory=dict)
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
        verified_using: List[IntegrityMethod] = None,
        external_reference: List[ExternalReference] = None,
        external_identifier: List[ExternalIdentifier] = None,
        extension: Optional[str] = None,
        build_id: Optional[str] = None,
        config_source_entrypoint: List[str] = None,
        config_source_uri: List[str] = None,
        config_source_digest: List[Hash] = None,
        parameters: Dict[str, str] = None,
        build_start_time: Optional[datetime] = None,
        build_end_time: Optional[datetime] = None,
        environment: Dict[str, str] = None,
    ):
        verified_using = [] if verified_using is None else verified_using
        external_reference = [] if external_reference is None else external_reference
        external_identifier = [] if external_identifier is None else external_identifier
        config_source_entrypoint = [] if config_source_entrypoint is None else config_source_entrypoint
        config_source_uri = [] if config_source_uri is None else config_source_uri
        config_source_digest = [] if config_source_digest is None else config_source_digest
        parameters = {} if parameters is None else parameters
        environment = {} if environment is None else environment

        check_types_and_set_values(self, locals())
