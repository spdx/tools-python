# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from copy import deepcopy

from beartype.typing import Any, Dict, List, Union

from spdx_tools.spdx.model import Document, File, Package, Snippet


def get_contained_spdx_element_ids(document: Document) -> List[str]:
    element_ids = [file.spdx_id for file in document.files]
    element_ids.extend([package.spdx_id for package in document.packages])
    element_ids.extend([snippet.spdx_id for snippet in document.snippets])
    return element_ids


def get_element_from_spdx_id(document: Document, spdx_id: str) -> Union[Package, File, Snippet, None]:
    contained_spdx_elements: Dict[str, Union[Package, File, Snippet]] = get_contained_spdx_elements(document)
    if spdx_id not in contained_spdx_elements:
        return None
    return contained_spdx_elements[spdx_id]


def get_contained_spdx_elements(document: Document) -> Dict[str, Union[Package, File, Snippet]]:
    contained_spdx_elements = {package.spdx_id: package for package in document.packages}
    contained_spdx_elements.update({file.spdx_id: file for file in document.files})
    contained_spdx_elements.update({snippet.spdx_id: snippet for snippet in document.snippets})

    return contained_spdx_elements


def create_document_without_duplicates(document: Document) -> Document:
    document_without_duplicates = deepcopy(document)
    for elements in [
        [document_without_duplicates.creation_info],
        document_without_duplicates.files,
        document_without_duplicates.packages,
        document_without_duplicates.snippets,
        document_without_duplicates.extracted_licensing_info,
    ]:
        for element in elements:
            for key, value in element.__dict__.items():
                if isinstance(value, list):
                    value_without_duplicates = create_list_without_duplicates(value)
                    setattr(element, key, value_without_duplicates)

    return document_without_duplicates


def create_list_without_duplicates(list_with_potential_duplicates: List[Any]) -> List[Any]:
    list_without_duplicates = []
    for element in list_with_potential_duplicates:
        if element not in list_without_duplicates:
            list_without_duplicates.append(element)

    return list_without_duplicates
