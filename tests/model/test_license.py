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


import pytest

from spdx.model.license import determine_full_name, determine_identifier


@pytest.mark.parametrize("identifier,full_name,expected",
                         [("0BSD", "full_name", "full_name"), (None, "full_name", "full_name"),
                          (None, "BSD Zero Clause License", "BSD Zero Clause License"),
                          ("0BSD", None, "BSD Zero Clause License"), ("identifier", None, "identifier")])
def test_determine_full_name(identifier, full_name, expected):
    assert determine_full_name(identifier, full_name) == expected


@pytest.mark.parametrize("identifier,full_name,expected",
                         [("identifier", "BSD Zero Clause License", "identifier"), (None, "full_name", "full_name"),
                          (None, "BSD Zero Clause License", "0BSD"), ("0BSD", None, "0BSD"),
                          ("identifier", None, "identifier")])
def test_determine_identifier(identifier, full_name, expected):
    assert determine_identifier(identifier, full_name) == expected
