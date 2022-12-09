import re
from typing import Optional, List

from src.model.document import Document
from src.validation.string_type_validators import is_valid_uri


def is_valid_spdx_id(spdx_id: str) -> bool:
    return bool(re.match(r"^SPDXRef-[\da-zA-Z.-]+$", spdx_id))


def is_spdx_id_present_in_document(spdx_id: str, document: Document) -> bool:
    id_list: List[str] = get_list_of_all_spdx_ids(document)

    return spdx_id in id_list


def get_list_of_all_spdx_ids(document: Document) -> List[str]:
    id_list: List[str] = [document.creation_info.spdx_id]

    id_list.extend([package.spdx_id for package in document.packages])
    id_list.extend([file.spdx_id for file in document.files])
    id_list.extend([snippet.spdx_id for snippet in document.snippets])

    return id_list


def validate_spdx_id_reference(spdx_id: str, document: Document) -> Optional[str]:
    split_id: List[str] = spdx_id.split(":")

    if len(split_id) > 2:
        return f'spdx_id must not contain more than one # in order to separate namespace from id, but is: {spdx_id}'

    if len(split_id) == 2:
        if not split_id[0]:
            return f'the namespace part of spdx_id must be a valid URI specified in RFC-3986, but is: {split_id[0]}'
        if not is_valid_spdx_id(split_id[1]):
            return f'the id part of spdx_id must be a valid SPDX id, but is: {split_id[1]}'

        if split_id[0] == document.creation_info.document_namespace:
            spdx_id = split_id[1]
        else:
            return None

    if is_spdx_id_present_in_document(spdx_id, document):
        return None

    return f'did not find spdx_id {spdx_id} in the SPDX document'
