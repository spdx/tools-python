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

from conversion.snippet_conversion import convert_snippet
from tests.fixtures import snippet_fixture
from spdx.model.snippet import Snippet as Snippet2
from spdx3.model.software.snippet import Snippet


@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_convert_snippet(creation_information):
    snippet2: Snippet2 = snippet_fixture()

    snippet: Snippet = convert_snippet(snippet2, creation_information=creation_information)

    assert snippet.spdx_id == "SPDXRef-Snippet"
