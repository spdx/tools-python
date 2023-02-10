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
import pytest

from spdx3.model.external_identifier import ExternalIdentifier, ExternalIdentifierType


def test_correct_initialization():
    external_identifier = ExternalIdentifier(ExternalIdentifierType.CPE22, "cpe:/o:canonical:ubuntu_linux:10.04:-:lts",
                                             "This is a comment")
    assert external_identifier.external_identifier_type == ExternalIdentifierType.CPE22
    assert external_identifier.identifier == "cpe:/o:canonical:ubuntu_linux:10.04:-:lts"
    assert external_identifier.comment == "This is a comment"


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        ExternalIdentifier("CPE22", ["identifier", "another_identifier"], 34)

    assert err.value.args[0] == ['SetterError ExternalIdentifier: type of argument "external_identifier_type" '
                                 'must be spdx3.model.external_identifier.ExternalIdentifierType; got str '
                                 'instead: CPE22',
                                 'SetterError ExternalIdentifier: type of argument "identifier" must be str; '
                                 "got list instead: ['identifier', 'another_identifier']",
                                 'SetterError ExternalIdentifier: type of argument "comment" must be one of '
                                 '(str, NoneType); got int instead: 34']
