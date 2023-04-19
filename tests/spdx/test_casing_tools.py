# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx.casing_tools import camel_case_to_snake_case, snake_case_to_camel_case


@pytest.mark.parametrize("snake_case_str,camel_case_str", [("snake_case", "snakeCase")])
def test_snake_case_to_camel_case(snake_case_str, camel_case_str):
    camel_case = snake_case_to_camel_case(snake_case_str)

    assert camel_case == camel_case_str


@pytest.mark.parametrize(
    "camel_case_str,snake_case_str",
    [("camelCase", "camel_case"), ("camelCaseMore", "camel_case_more"), ("CamelCase", "camel_case")],
)
def test_camel_case_to_snake_case(camel_case_str, snake_case_str):
    snake_case = camel_case_to_snake_case(camel_case_str)

    assert snake_case == snake_case_str
