# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import TextIO

from spdx_tools.spdx3.model import ExternalReference
from spdx_tools.spdx3.writer.console.console import write_value


def write_external_reference(external_reference: ExternalReference, text_output: TextIO):
    write_value("type", external_reference.external_reference_type.name, text_output)
    write_value("locator", ", ".join(external_reference.locator), text_output)
    write_value("content_type", external_reference.content_type, text_output)
    write_value("comment", external_reference.comment, text_output)
