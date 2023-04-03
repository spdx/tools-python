# SPDX-FileCopyrightText: 2023 spdx contributors

# SPDX-License-Identifier: Apache-2.0
from typing import TextIO

from spdx3.model.namespace_map import NamespaceMap
from spdx3.writer.console.console import write_value


def write_namespace_map(namespace_map: NamespaceMap, text_output: TextIO):
    write_value("prefix", namespace_map.prefix, text_output)
    write_value("namespace", namespace_map.namespace, text_output)
