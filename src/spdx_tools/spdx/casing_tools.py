# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from re import sub


def snake_case_to_camel_case(snake_case_string: str) -> str:
    each_word_capitalized = sub(r"[_\-]+", " ", snake_case_string).title().replace(" ", "")
    return each_word_capitalized[0].lower() + each_word_capitalized[1:]


def camel_case_to_snake_case(camel_case_string: str) -> str:
    snake_case_string = sub("(?!^)([A-Z]+)", r"_\1", camel_case_string).lower()
    return snake_case_string
