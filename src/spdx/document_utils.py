# SPDX-FileCopyrightText: 2022 spdx contributors

# SPDX-License-Identifier: Apache-2.0
from typing import List, Union

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
    elements = [file_ for file_ in document.files]
    elements.extend([package_ for package_ in document.packages])
    elements.extend([snippet_ for snippet_ in document.snippets])
    for element in elements:
        if element.spdx_id == spdx_id:
            return element
