# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import TextIO

from spdx_tools.spdx3.model.external_identifier import ExternalIdentifier
from spdx_tools.spdx3.writer.console.console import write_value


def write_external_identifier(external_identifier: ExternalIdentifier, text_output: TextIO):
    write_value("type", external_identifier.external_identifier_type.name, text_output)
    write_value("identifier", external_identifier.identifier, text_output)
    write_value("comment", external_identifier.comment, text_output)
