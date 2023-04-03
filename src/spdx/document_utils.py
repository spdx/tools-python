# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import Dict, List, Union

from spdx.model.document import Document
from spdx.model.file import File
from spdx.model.package import Package
from spdx.model.snippet import Snippet


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
