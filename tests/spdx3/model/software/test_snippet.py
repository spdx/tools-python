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

from spdx3.model.software.snippet import Snippet


@mock.patch("spdx3.model.software.snippet.Snippet", autospec=True)
def test_correct_initialization(creation_information):
    snippet = Snippet("SPDXRef-Snippet", creation_information, content_identifier="https://content.identifier",
                      snippet_purpose=[SoftwarePurpose.SOURCE], byte_range=(3, 4), line_range=(346, 456))

    assert snippet.spdx_id == "SPDXRef-Snippet"
    assert snippet.creation_info == creation_information
    assert snippet.content_identifier == "https://content.identifier"
    assert snippet.snippet_purpose == [SoftwarePurpose.SOURCE]
    assert snippet.byte_range == (3, 4)
    assert snippet.line_range == (346, 456)


@mock.patch("spdx3.model.software.snippet.Snippet", autospec=True)
def test_invalid_initialization(creation_information):
    with pytest.raises(TypeError) as err:
        Snippet(2, creation_information, originated_by=34, byte_range="34:45")

    assert err.value.args[0] == ['SetterError Snippet: type of argument "spdx_id" must be str; got int '
                                 'instead: 2',
                                 'SetterError Snippet: type of argument "originated_by" must be one of (str, '
                                 'NoneType); got int instead: 34',
                                 'SetterError Snippet: type of argument "byte_range" must be one of '
                                 '(Tuple[int, int], NoneType); got str instead: 34:45']
