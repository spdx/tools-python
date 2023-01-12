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

from conversion.file_conversion import convert_file
from spdx3.model.software.file import File

from tests.fixtures import file_fixture
from spdx.model.file import File as File2


@mock.patch("spdx3.model.creation_information.CreationInformation")
def test_convert_file(creation_information):
    file2: File2 = file_fixture()

    file: File = convert_file(file2, creation_information=creation_information)

    assert file.spdx_id == "SPDXRef-File"
