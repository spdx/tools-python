# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model import NamespaceMap
from spdx_tools.spdx3.writer.console.console import write_value


def write_namespace_map(namespace_map: NamespaceMap, text_output: TextIO):
    for property_name in NamespaceMap.__annotations__.keys():
        write_value(property_name, getattr(namespace_map, property_name), text_output)
