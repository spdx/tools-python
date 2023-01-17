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

from spdx3.model.integrity_method import IntegrityMethod


def test_correct_initialization():
    integrity_method = IntegrityMethod(comment="This is a comment.")

    assert integrity_method.comment == "This is a comment."


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        IntegrityMethod(["some comments", "and some more comments"])

    assert err.value.args[0] == ['SetterError IntegrityMethod: type of argument "comment" must be one of (str, '
                                 "NoneType); got list instead: ['some comments', 'and some more comments']"]
