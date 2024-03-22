# SPDX-License-Identifier: Apache-2.0
#  Copyright (c) 2022 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from beartype.typing import Any, Callable, Dict, List, Optional, TextIO, Tuple, Union
from license_expression import LicenseExpression

from spdx_tools.spdx.model import (
    Actor,
    File,
    Package,
    Relationship,
    RelationshipType,
    Snippet,
    SpdxNoAssertion,
    SpdxNone,
)


def write_separator(out: TextIO):
    out.write("\n")


def write_value(
    tag: str, value: Optional[Union[bool, str, SpdxNone, SpdxNoAssertion, LicenseExpression]], out: TextIO
):
    if value is not None:
        out.write(f"{tag}: {value}\n")


def write_range(tag: str, value: Optional[Tuple[int, int]], out: TextIO):
    if value:
        out.write(f"{tag}: {value[0]}:{value[1]}\n")


def write_text_value(tag: str, value: Optional[Union[str, SpdxNone, SpdxNoAssertion]], out: TextIO):
    if isinstance(value, str) and "\n" in value:
        out.write(f"{tag}: <text>{value}</text>\n")
    else:
        write_value(tag, value, out)


def transform_enum_name_to_tv(enum_str: str) -> str:
    return enum_str.replace("_", "-")


def write_optional_heading(optional_field: Any, heading: str, text_output: TextIO):
    if optional_field:
        text_output.write(heading)


def write_list_of_elements(
    list_of_elements: List[Any],
    write_method: Callable[[Any, TextIO], None],
    text_output: TextIO,
    with_separator: bool = False,
):
    for element in list_of_elements:
        write_method(element, text_output)
        if with_separator:
            write_separator(text_output)


def write_actor(tag: str, element_to_write: Optional[Union[Actor, SpdxNoAssertion]], text_output: TextIO):
    if isinstance(element_to_write, Actor):
        write_value(tag, element_to_write.to_serialized_string(), text_output)
    else:
        write_value(tag, element_to_write, text_output)


def scan_relationships(
    relationships: List[Relationship], packages: List[Package], files: List[File]
) -> Tuple[List, Dict]:
    contained_files_by_package_id = dict()
    relationships_to_write = []
    files_by_spdx_id = {file.spdx_id: file for file in files}
    packages_spdx_ids = [package.spdx_id for package in packages]
    for relationship in relationships:
        if relationship.related_spdx_element_id in [SpdxNoAssertion(), SpdxNone()]:
            relationships_to_write.append(relationship)
        elif (
            relationship.relationship_type == RelationshipType.CONTAINS
            and relationship.spdx_element_id in packages_spdx_ids
            and relationship.related_spdx_element_id in files_by_spdx_id.keys()
        ):
            contained_files_by_package_id.setdefault(relationship.spdx_element_id, []).append(
                files_by_spdx_id[relationship.related_spdx_element_id]
            )
            if relationship.comment:
                relationships_to_write.append(relationship)
        elif (
            relationship.relationship_type == RelationshipType.CONTAINED_BY
            and relationship.related_spdx_element_id in packages_spdx_ids
            and relationship.spdx_element_id in files_by_spdx_id
        ):
            contained_files_by_package_id.setdefault(relationship.related_spdx_element_id, []).append(
                files_by_spdx_id[relationship.spdx_element_id]
            )
            if relationship.comment:
                relationships_to_write.append(relationship)
        else:
            relationships_to_write.append(relationship)

    return relationships_to_write, contained_files_by_package_id


def get_file_ids_with_contained_snippets(snippets: List[Snippet], files: List[File]) -> Dict:
    file_ids_with_contained_snippets = dict()
    file_spdx_ids: List[str] = [file.spdx_id for file in files]
    for snippet in snippets:
        if snippet.file_spdx_id in file_spdx_ids:
            file_ids_with_contained_snippets.setdefault(snippet.file_spdx_id, []).append(snippet)

    return file_ids_with_contained_snippets
