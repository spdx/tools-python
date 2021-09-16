# Copyright (c) 2021 spdx tool contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from spdx.parsers.loggers import ErrorMessages


def test_error_message_context():
    messages = ErrorMessages()
    messages.push_context("package1")
    messages.append("missing value: {0} {bar}", "foo", bar="bar")
    messages.append("missing key")
    messages.pop_context()
    messages.append("lone message")
    messages.push_context("package2")
    messages.push_context("file1")
    messages.append("more message")
    assert messages.messages == [
        "package1: missing value: foo bar",
        "package1: missing key",
        "lone message",
        "package2: file1: more message",
    ]
