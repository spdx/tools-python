#  Copyright (c) 2023 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from unittest import mock

from spdx3.bump_from_spdx2.file import bump_file
from spdx3.model.integrity_method import IntegrityMethod, Hash, HashAlgorithm
from spdx3.model.software.file import File

from tests.fixtures import file_fixture
from spdx.model.file import File as Spdx2_File

@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_bump_file(creation_information):
    spdx2_file: Spdx2_File = file_fixture()
    integrity_method: Hash = Hash(HashAlgorithm.SHA1, "71c4025dd9897b364f3ebbb42c484ff43d00791c")

    file: File = bump_file(spdx2_file, creation_information=creation_information)

    assert file.spdx_id == "SPDXRef-File"
    assert file.verified_using == [integrity_method]
