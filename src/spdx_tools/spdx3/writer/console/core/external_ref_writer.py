# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model.core import ExternalRef
from spdx_tools.spdx3.writer.console.console import write_value


def write_external_ref(external_ref: ExternalRef, text_output: TextIO):
    for property_name in ExternalRef.__annotations__.keys():
        write_value(property_name, getattr(external_ref, property_name), text_output)
