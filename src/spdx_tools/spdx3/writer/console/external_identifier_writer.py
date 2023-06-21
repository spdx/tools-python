# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model import ExternalIdentifier
from spdx_tools.spdx3.writer.console.console import write_value


def write_external_identifier(external_identifier: ExternalIdentifier, text_output: TextIO):
    for property_name in ExternalIdentifier.__annotations__.keys():
        write_value(property_name, getattr(external_identifier, property_name), text_output)
