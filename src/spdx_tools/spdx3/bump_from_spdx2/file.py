# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from spdx_tools.spdx3.bump_from_spdx2.checksum import bump_checksum
from spdx_tools.spdx3.bump_from_spdx2.message import print_missing_conversion
from spdx_tools.spdx3.model.creation_information import CreationInformation
from spdx_tools.spdx3.model.software.file import File
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx.model.file import File as Spdx2_File


def bump_file(
    spdx2_file: Spdx2_File, payload: Payload, creation_information: CreationInformation, document_namespace: str
):
    spdx_id = "#".join([document_namespace, spdx2_file.spdx_id])
    name = spdx2_file.name
    integrity_methods = [bump_checksum(checksum) for checksum in spdx2_file.checksums]
    # file.checksums -> file.verifiedUsing
    # file.file_types -> file.content_type (MediaType with Cardinality 1)
    print_missing_conversion("file.file_type", 0, "different cardinalities")
    print_missing_conversion(
        "file.concluded_license, file.license_info_in_file, file.license_comment, file.copyright_text",
        0,
        "missing definition for license profile",
    )

    comment = spdx2_file.comment
    print_missing_conversion(
        "file.notice, file.contributors, file.attribution_texts", 0, "missing definition for license profile"
    )

    payload.add_element(
        File(spdx_id, creation_info=creation_information, name=name, comment=comment, verified_using=integrity_methods)
    )
