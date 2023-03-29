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
from re import sub


def snake_case_to_camel_case(snake_case_string: str) -> str:
    each_word_capitalized = sub(r"[_\-]+", " ", snake_case_string).title().replace(" ", "")
    return each_word_capitalized[0].lower() + each_word_capitalized[1:]


def camel_case_to_snake_case(camel_case_string: str) -> str:
    snake_case_string = sub("(?!^)([A-Z]+)", r"_\1", camel_case_string).lower()
    return snake_case_string
