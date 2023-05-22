# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import List, Union

from spdx_tools.spdx3.model import ExternalMap
from spdx_tools.spdx.model import ExternalDocumentRef, File, Package, Snippet


def get_full_element_spdx_id_and_set_imports(
    element: Union[Package, File, Snippet],
    document_namespace: str,
    external_document_refs: List[ExternalDocumentRef],
    imports: List[ExternalMap],
) -> str:
    """
    Returns the spdx_id of the element prefixed with the correct document namespace and,
    if the element is from an external document, sets the correct entry in the imports property.
    """
    if ":" not in element.spdx_id:
        return f"{document_namespace}#{element.spdx_id}"

    external_id, local_id = element.spdx_id.split(":")
    external_uri = None
    for entry in external_document_refs:
        if entry.document_ref_id == external_id:
            external_uri = entry.document_uri
            break

    if external_uri:
        imports.append(ExternalMap(external_id=element.spdx_id, defining_document=f"{external_id}:SPDXRef-DOCUMENT"))
        return external_uri + "#" + local_id

    raise ValueError(f"external id {external_id} not found in external document references")
