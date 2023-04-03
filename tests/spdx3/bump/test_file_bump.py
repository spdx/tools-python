# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from unittest import mock

from spdx3.bump_from_spdx2.file import bump_file
from spdx3.model.hash import Hash, HashAlgorithm
from spdx3.model.software.file import File
from spdx3.payload import Payload
from spdx.model.file import File as Spdx2_File
from tests.spdx.fixtures import file_fixture


@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_bump_file(creation_information):
    payload = Payload()
    document_namespace = "https://doc.namespace"
    spdx2_file: Spdx2_File = file_fixture()
    integrity_method: Hash = Hash(HashAlgorithm.SHA1, "71c4025dd9897b364f3ebbb42c484ff43d00791c")
    expected_new_file_id = f"{document_namespace}#{spdx2_file.spdx_id}"

    bump_file(spdx2_file, payload, creation_information, document_namespace)
    file = payload.get_element(expected_new_file_id)

    assert isinstance(file, File)
    assert file.spdx_id == expected_new_file_id
    assert file.verified_using == [integrity_method]
