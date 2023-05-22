# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import mock

from spdx_tools.spdx3.bump_from_spdx2.file import bump_file
from spdx_tools.spdx3.model import Hash, HashAlgorithm
from spdx_tools.spdx3.model.licensing import ConjunctiveLicenseSet, ListedLicense
from spdx_tools.spdx3.model.software import File
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx.model.file import File as Spdx2_File
from tests.spdx.fixtures import file_fixture


@mock.patch("spdx_tools.spdx3.model.CreationInfo", autospec=True)
def test_bump_file(creation_info):
    payload = Payload()
    document_namespace = "https://doc.namespace"
    spdx2_file: Spdx2_File = file_fixture()
    integrity_method: Hash = Hash(HashAlgorithm.SHA1, "71c4025dd9897b364f3ebbb42c484ff43d00791c")
    expected_new_file_id = f"{document_namespace}#{spdx2_file.spdx_id}"

    bump_file(spdx2_file, payload, creation_info, document_namespace, [], [], [])
    file = payload.get_element(expected_new_file_id)

    assert isinstance(file, File)
    assert file.spdx_id == expected_new_file_id
    assert file.verified_using == [integrity_method]
    assert file.concluded_license == ConjunctiveLicenseSet(
        [ListedLicense("MIT", "MIT", ""), ListedLicense("GPL-2.0-only", "GPL-2.0-only", "")]
    )
    assert file.copyright_text == spdx2_file.copyright_text
    assert file.attribution_text == spdx2_file.attribution_texts[0]
