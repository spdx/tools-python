# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from spdx_tools.spdx3.bump_from_spdx2.annotation import bump_annotation
from spdx_tools.spdx3.bump_from_spdx2.creation_info import bump_creation_info
from spdx_tools.spdx3.bump_from_spdx2.file import bump_file
from spdx_tools.spdx3.bump_from_spdx2.package import bump_package
from spdx_tools.spdx3.bump_from_spdx2.relationship import bump_relationships
from spdx_tools.spdx3.bump_from_spdx2.snippet import bump_snippet
from spdx_tools.spdx3.model import CreationInfo, SpdxDocument
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx.model import RelationshipType
from spdx_tools.spdx.model.document import Document as Spdx2_Document
from spdx_tools.spdx.model.relationship_filters import filter_by_type_and_origin

""" We want to implement a bump_from_spdx2 from the data model in src.spdx to the data model in src.spdx3.
    As there are many fundamental differences between these version we want each bump_from_spdx2 method to take
    the object from src.spdx and add all objects that the input is translated to into the payload."""


def bump_spdx_document(document: Spdx2_Document) -> Payload:
    payload = Payload()
    document_namespace: str = document.creation_info.document_namespace
    spdx_document: SpdxDocument = bump_creation_info(document.creation_info, payload)
    spdx_document.root_element = [
        f"{document_namespace}#{relationship.related_spdx_element_id}"
        for relationship in filter_by_type_and_origin(
            document.relationships, RelationshipType.DESCRIBES, "SPDXRef-DOCUMENT"
        )
    ]

    creation_info: CreationInfo = spdx_document.creation_info

    payload.add_element(spdx_document)

    for spdx2_package in document.packages:
        bump_package(
            spdx2_package,
            payload,
            document_namespace,
            document.creation_info.external_document_refs,
            spdx_document.imports,
        )

    for spdx2_file in document.files:
        bump_file(
            spdx2_file,
            payload,
            document_namespace,
            document.creation_info.external_document_refs,
            spdx_document.imports,
        )

    for spdx2_snippet in document.snippets:
        bump_snippet(
            spdx2_snippet,
            payload,
            document_namespace,
            document.creation_info.external_document_refs,
            spdx_document.imports,
        )

    bump_relationships(document.relationships, payload, document_namespace)

    for counter, spdx2_annotation in enumerate(document.annotations):
        bump_annotation(spdx2_annotation, payload, creation_info, document_namespace, counter)

    spdx_document.element = [spdx_id for spdx_id in payload.get_full_map() if spdx_id != spdx_document.spdx_id]

    return payload
