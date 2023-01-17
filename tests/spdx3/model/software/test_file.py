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

import pytest

from spdx3.model.software.software_purpose import SoftwarePurpose

from spdx3.model.software.file import File


@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_correct_initialization(creation_information):
    file = File("SPDXRef-File", creation_information, content_identifier="https://any.uri",
                file_purpose=[SoftwarePurpose.ARCHIVE, SoftwarePurpose.FILE], content_type="MediaType")

    assert file.spdx_id == "SPDXRef-File"
    assert file.creation_info == creation_information
    assert file.content_identifier == "https://any.uri"
    assert file.file_purpose == [SoftwarePurpose.ARCHIVE, SoftwarePurpose.FILE]
    assert file.content_type == "MediaType"


@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_invalid_initialization(creation_information):
    with pytest.raises(TypeError) as err:
        File(1, creation_information, content_identifier=3, file_purpose=SoftwarePurpose.FILE,
             content_type=SoftwarePurpose.ARCHIVE)

    assert err.value.args[0] == ['SetterError File: type of argument "spdx_id" must be str; got int instead: 1',
                                 'SetterError File: type of argument "content_identifier" must be one of (str, '
                                 'NoneType); got int instead: 3',
                                 'SetterError File: type of argument "file_purpose" must be one of '
                                 '(List[spdx3.model.software.software_purpose.SoftwarePurpose], NoneType); got '
                                 'spdx3.model.software.software_purpose.SoftwarePurpose instead: '
                                 'SoftwarePurpose.FILE',
                                 'SetterError File: type of argument "content_type" must be one of (str, '
                                 'NoneType); got spdx3.model.software.software_purpose.SoftwarePurpose '
                                 'instead: SoftwarePurpose.ARCHIVE']
