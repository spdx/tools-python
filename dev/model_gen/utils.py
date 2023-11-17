# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import os
import textwrap

import mistletoe
from beartype.typing import Optional
from mistletoe.markdown_renderer import MarkdownRenderer

from spdx_tools.spdx.casing_tools import camel_case_to_snake_case

SPECIAL_TYPE_MAPPINGS: dict[str, tuple[str, Optional[str]]] = {
    "Core/DateTime": ("datetime", "datetime"),
    "Core/DictionaryEntry": ("Dict[str, Optional[str]]", None),
    "Core/Extension": ("str", None),
    "Core/MediaType": ("str", None),
    "Core/SemVer": ("Version", "semantic_version"),
    "xsd:anyURI": ("str", None),
    "xsd:boolean": ("bool", None),
    "xsd:datetime": ("datetime", "datetime"),
    "xsd:decimal": ("float", None),
    "xsd:double": ("float", None),
    "xsd:float": ("float", None),
    "xsd:int": ("int", None),
    "xsd:integer": ("int", None),
    "xsd:negativeInteger": ("int", None),
    "xsd:nonNegativeInteger": ("int", None),
    "xsd:nonPositiveInteger": ("int", None),
    "xsd:positiveInteger": ("int", None),
    "xsd:string": ("str", None),
}


def prop_name_to_python(prop_name: str):
    special_cases = {"from": "from_element", "homePage": "homepage"}
    prop_name = get_short_prop_name(prop_name)
    if prop_name in special_cases:
        return special_cases[prop_name]
    return camel_case_to_snake_case(prop_name)


def namespace_name_to_python(namespace_name: str):
    special_cases = {"AI": "ai"}
    if namespace_name in special_cases:
        return special_cases[namespace_name]
    return camel_case_to_snake_case(namespace_name)


def get_file_path(typename: str, namespace: str, output_dir: str) -> str:
    namespace = namespace_name_to_python(namespace)
    typename = camel_case_to_snake_case(typename) if typename != "AIPackage" else "ai_package"
    return os.path.join(output_dir, namespace, f"{typename}.py")


def get_python_docstring(description: Optional[str], indent: int) -> str:
    if not description:
        return ""

    line_length = 119 - indent
    with MarkdownRenderer(max_line_length=line_length) as renderer:
        text = renderer.render(mistletoe.Document(description))
    text = '\n"""\n' + text + '"""'
    return textwrap.indent(text, ' ' * indent)


def get_qualified_name(name: str, namespace: str):
    if name.startswith('/'):
        name = name[1:]
    if name.startswith("xsd:"):
        return name
    if '/' in name:
        return name
    return f"{namespace}/{name}"


def split_qualified_name(typename: str) -> tuple[str, str]:
    if '/' not in typename:
        return "", typename
    namespace, _, typename = typename.partition('/')
    return namespace, typename


def to_python_type(typename: str) -> str:
    if typename in SPECIAL_TYPE_MAPPINGS:
        return SPECIAL_TYPE_MAPPINGS[typename][0]
    if typename.startswith("xsd:"):
        return "str"
    _, typename = split_qualified_name(typename)
    return typename


def extract_parent_type(cls: dict, namespace: str) -> Optional[str]:
    parent_class = cls["metadata"].get("SubclassOf") or "none"
    if parent_class == "none" or parent_class == "owl:Thing":
        return None
    return get_qualified_name(parent_class, namespace)


def get_short_prop_name(qualified_name: str) -> str:
    if '/' not in qualified_name:
        return qualified_name
    return qualified_name[qualified_name.rindex('/') + 1:]
