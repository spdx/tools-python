# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import hashlib

from beartype.typing import List, Optional, Type, Union

from spdx_tools.spdx.model import (
    ChecksumAlgorithm,
    Document,
    ExternalDocumentRef,
    File,
    Package,
    PackageVerificationCode,
    Snippet,
)


def get_element_type_from_spdx_id(
    spdx_id: str, document: Document
) -> Optional[Union[Type[Package], Type[File], Type[Snippet]]]:
    if spdx_id in [package.spdx_id for package in document.packages]:
        return Package
    if spdx_id in [file.spdx_id for file in document.files]:
        return File
    if spdx_id in [snippet.spdx_id for snippet in document.snippets]:
        return Snippet
    return None


def get_full_element_spdx_id(
    element: Union[Package, File, Snippet],
    document_namespace: str,
    external_document_refs: List[ExternalDocumentRef],
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

    if not external_uri:
        raise ValueError(f"external id {external_id} not found in external document references")

    return external_uri + "#" + local_id


def calculate_package_verification_code(files: List[File]) -> PackageVerificationCode:
    list_of_file_hashes = []
    for file in files:
        file_checksum_value = None
        for checksum in file.checksums:
            if checksum.algorithm == ChecksumAlgorithm.SHA1:
                file_checksum_value = checksum.value
        if not file_checksum_value:
            try:
                file_checksum_value = calculate_file_checksum(file.name, ChecksumAlgorithm.SHA1)
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"Cannot calculate package verification code because the file '{file.name}' "
                    f"provides no SHA1 checksum and can't be found at the specified location."
                )
        list_of_file_hashes.append(file_checksum_value)

    list_of_file_hashes.sort()
    hasher = hashlib.new("sha1")
    hasher.update("".join(list_of_file_hashes).encode("utf-8"))
    value = hasher.hexdigest()
    return PackageVerificationCode(value)


def calculate_file_checksum(file_name: str, hash_algorithm=ChecksumAlgorithm.SHA1) -> str:
    BUFFER_SIZE = 65536

    file_hash = hashlib.new(hash_algorithm.name.lower())
    with open(file_name, "rb") as file_handle:
        while True:
            data = file_handle.read(BUFFER_SIZE)
            if not data:
                break
            file_hash.update(data)

    return file_hash.hexdigest()
