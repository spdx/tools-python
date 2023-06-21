# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model import CreationInfo
from spdx_tools.spdx3.writer.console.console import write_value
from spdx_tools.spdx.datetime_conversions import datetime_to_iso_string


def write_creation_info(creation_info: CreationInfo, text_output: TextIO, indent: bool = True):
    text_output.write("# Creation Information\n")
    write_value("specVersion", str(creation_info.spec_version), text_output, indent)
    write_value("created", datetime_to_iso_string(creation_info.created), text_output, indent)
    for created_by in creation_info.created_by:
        write_value("created by", created_by, text_output, indent)
    for created_using in creation_info.created_using:
        write_value("created using", created_using, text_output, indent)
    write_value("profile", [profile.name for profile in creation_info.profile], text_output, indent)
    write_value("data license", creation_info.data_license, text_output, indent)
    write_value("comment", creation_info.comment, text_output, indent)
