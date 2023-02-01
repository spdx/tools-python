# Copyright (c) 2022 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
from typing import List

from spdx.document_utils import get_contained_spdx_element_ids
from spdx.model.document import Document
from spdx.model.file import File


def is_valid_internal_spdx_id(spdx_id: str) -> bool:
    return bool(re.match(r"^SPDXRef-[\da-zA-Z.-]+$", spdx_id))


def is_valid_external_doc_ref_id(external_ref_id: str) -> bool:
    return bool(re.match(r"^DocumentRef-[\da-zA-Z.+-]+$", external_ref_id))


def is_spdx_id_present_in_files(spdx_id: str, files: List[File]) -> bool:
    return spdx_id in [file.spdx_id for file in files]


def is_spdx_id_present_in_document(spdx_id: str, document: Document) -> bool:
    all_spdx_ids_in_document: List[str] = get_list_of_all_spdx_ids(document)

    return spdx_id in all_spdx_ids_in_document


def get_list_of_all_spdx_ids(document: Document) -> List[str]:
    all_spdx_ids_in_document: List[str] = [document.creation_info.spdx_id]
    all_spdx_ids_in_document.extend(get_contained_spdx_element_ids(document))

    return all_spdx_ids_in_document


def is_external_doc_ref_present_in_document(external_ref_id: str, document: Document) -> bool:
    all_external_doc_ref_ids_in_document = [external_doc_ref.document_ref_id for external_doc_ref in
                                            document.creation_info.external_document_refs]

    return external_ref_id in all_external_doc_ref_ids_in_document


def validate_spdx_id(spdx_id: str, document: Document, check_document: bool = False, check_files: bool = False) -> List[
    str]:
    """ Test that the given spdx_id (and a potential DocumentRef to an external document) is valid
    and, if it is a reference, actually exists in the document. Optionally checks files or the whole document
    for the existence of the spdx_id (i.e. if it is used as a reference). Returns a list of validation messages. """

    validation_messages: List[str] = []
    split_id: List[str] = spdx_id.split(":")

    # # # invalid case # # #
    if len(split_id) > 2:
        return [
            f"spdx_id must not contain more than one colon in order to separate the external document reference id from the internal SPDX id, but is: {spdx_id}"]

    # # # case with external document ref prefix # # #
    if len(split_id) == 2:
        if not is_valid_external_doc_ref_id(split_id[0]):
            validation_messages.append(
                f'the external document reference part of spdx_id must only contain letters, numbers, ".", "-" and "+" and must begin with "DocumentRef-", but is: {split_id[0]}')
        if not is_valid_internal_spdx_id(split_id[1]):
            validation_messages.append(
                f'the internal SPDX id part of spdx_id must only contain letters, numbers, "." and "-" and must begin with "SPDXRef-", but is: {split_id[1]}')
        if not is_external_doc_ref_present_in_document(split_id[0], document):
            validation_messages.append(
                f'did not find the external document reference "{split_id[0]}" in the SPDX document')

        return validation_messages

    # # # "normal" case # # #
    if not is_valid_internal_spdx_id(spdx_id):
        validation_messages.append(
            f'spdx_id must only contain letters, numbers, "." and "-" and must begin with "SPDXRef-", but is: {spdx_id}')

    if check_document:
        if not is_spdx_id_present_in_document(spdx_id, document):
            validation_messages.append(f'did not find the referenced spdx_id "{spdx_id}" in the SPDX document')

    if check_files:
        if not is_spdx_id_present_in_files(spdx_id, document.files):
            validation_messages.append(f'did not find the referenced spdx_id "{spdx_id}" in the SPDX document\'s files')

    return validation_messages
