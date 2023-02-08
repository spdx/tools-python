# Copyright (c) 2023 spdx contributors
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

from spdx.casing_tools import snake_case_to_camel_case, camel_case_to_snake_case


@pytest.mark.parametrize("snake_case_str,camel_case_str", [("snake_case", "snakeCase")])
def test_snake_case_to_camel_case(snake_case_str, camel_case_str):
    camel_case = snake_case_to_camel_case(snake_case_str)

    assert camel_case == camel_case_str


@pytest.mark.parametrize("camel_case_str,snake_case_str",
                         [("camelCase", "camel_case"), ("camelCaseMore", "camel_case_more"),
                          ("CamelCase", "camel_case")])
def test_camel_case_to_snake_case(camel_case_str, snake_case_str):
    snake_case = camel_case_to_snake_case(camel_case_str)

    assert snake_case == snake_case_str
