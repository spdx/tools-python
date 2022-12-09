import re
from typing import Optional, List

from src.model.document import Document
from src.validation.uri_validator import is_valid_uri


def is_valid_spdx_id(spdx_id: str) -> bool:
    return bool(re.match(r"^SPDXRef-[\da-zA-Z.-]+$", spdx_id))


def is_valid_external_doc_ref_id(external_ref_id: str) -> bool:
    return bool(re.match(r"^DocumentRef-[\da-zA-Z.+-]+$", external_ref_id))


def is_spdx_id_present_in_document(spdx_id: str, document: Document) -> bool:
    all_spdx_ids_in_document: List[str] = get_list_of_all_spdx_ids(document)

    return spdx_id in all_spdx_ids_in_document


def get_list_of_all_spdx_ids(document: Document) -> List[str]:
    all_spdx_ids_in_document: List[str] = [document.creation_info.spdx_id]

    all_spdx_ids_in_document.extend([package.spdx_id for package in document.packages])
    all_spdx_ids_in_document.extend([file.spdx_id for file in document.files])
    all_spdx_ids_in_document.extend([snippet.spdx_id for snippet in document.snippets])

    return all_spdx_ids_in_document


def is_external_doc_ref_present_in_document(external_ref_id: str, document: Document) -> bool:
    all_external_doc_ref_ids_in_document = [external_doc_ref.document_ref_id for external_doc_ref in document.creation_info.external_document_refs]

    return external_ref_id in all_external_doc_ref_ids_in_document


def validate_spdx_id_reference(spdx_id: str, document: Document) -> Optional[str]:
    split_id: List[str] = spdx_id.split(":")

    if len(split_id) > 2:
        return f'spdx_id must not contain more than one colon in order to separate the external document reference id from the internal SPDX id, but is: {spdx_id}'

    if len(split_id) == 2:
        if not is_valid_external_doc_ref_id(split_id[0]):
            return f'the external document reference part of spdx_id must only contain letters, numbers, ".", "-" and "+" and must begin with "DocumentRef-", but is: {split_id[0]}'
        if not is_external_doc_ref_present_in_document(split_id[0]):
            return f'did not find the external document reference {split_id[0]} in the SPDX document'
        if not is_valid_spdx_id(split_id[1]):
            return f'the id part of spdx_id must only contain letters, numbers, "." and "-" and must begin with "SPDXRef-", but is: {split_id[1]}'

        if split_id[0] == document.creation_info.document_namespace:
            spdx_id = split_id[1]
        else:
            return None

    if is_spdx_id_present_in_document(spdx_id, document):
        return None

    return f'did not find the referenced spdx_id {spdx_id} in the SPDX document'
