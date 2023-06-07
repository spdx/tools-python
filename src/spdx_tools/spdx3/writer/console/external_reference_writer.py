# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model import ExternalReference
from spdx_tools.spdx3.writer.console.console import write_value


def write_external_reference(external_reference: ExternalReference, text_output: TextIO):
    for property_name in ExternalReference.__annotations__.keys():
        write_value(property_name, getattr(external_reference, property_name), text_output)
