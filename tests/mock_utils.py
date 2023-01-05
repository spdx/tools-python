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
from unittest.mock import NonCallableMagicMock


def assert_mock_method_called_with_arguments(mock_object: NonCallableMagicMock, method_name: str, *args):
    assert len(mock_object.method_calls) == len(args)
    for running_index in range(len(args)):
        call = mock_object.method_calls[running_index]
        assert call[0] == method_name
        assert call[1][0] == args[running_index]


def assert_no_mock_methods_called(mock_object: NonCallableMagicMock):
    assert len(mock_object.method_calls) == 0
