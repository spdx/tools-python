# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from dataclasses import field
from datetime import datetime

from beartype.typing import List, Optional

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx.model import (
    Actor,
    Annotation,
    ExternalDocumentRef,
    ExtractedLicensingInfo,
    File,
    Package,
    Relationship,
    Snippet,
    Version,
)


@dataclass_with_properties
class CreationInfo:
    spdx_version: str
    spdx_id: str
    name: str
    document_namespace: str
    creators: List[Actor]
    created: datetime
    creator_comment: Optional[str] = None
    data_license: str = "CC0-1.0"
    external_document_refs: List[ExternalDocumentRef] = field(default_factory=list)
    license_list_version: Optional[Version] = None
    document_comment: Optional[str] = None

    def __init__(
        self,
        spdx_version: str,
        spdx_id: str,
        name: str,
        document_namespace: str,
        creators: List[Actor],
        created: datetime,
        creator_comment: Optional[str] = None,
        data_license: str = "CC0-1.0",
        external_document_refs: List[ExternalDocumentRef] = None,
        license_list_version: Optional[Version] = None,
        document_comment: Optional[str] = None,
    ):
        external_document_refs = [] if external_document_refs is None else external_document_refs
        check_types_and_set_values(self, locals())


@dataclass_with_properties
class Document:
    creation_info: CreationInfo

    packages: List[Package] = field(default_factory=list)
    files: List[File] = field(default_factory=list)
    snippets: List[Snippet] = field(default_factory=list)
    annotations: List[Annotation] = field(default_factory=list)
    relationships: List[Relationship] = field(default_factory=list)
    extracted_licensing_info: List[ExtractedLicensingInfo] = field(default_factory=list)

    def __init__(
        self,
        creation_info: CreationInfo,
        packages: List[Package] = None,
        files: List[File] = None,
        snippets: List[Snippet] = None,
        annotations: List[Annotation] = None,
        relationships: List[Relationship] = None,
        extracted_licensing_info: List[ExtractedLicensingInfo] = None,
    ):
        packages = [] if packages is None else packages
        files = [] if files is None else files
        snippets = [] if snippets is None else snippets
        annotations = [] if annotations is None else annotations
        relationships = [] if relationships is None else relationships
        extracted_licensing_info = [] if extracted_licensing_info is None else extracted_licensing_info
        check_types_and_set_values(self, locals())
