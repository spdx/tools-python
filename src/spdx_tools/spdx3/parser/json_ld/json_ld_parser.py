# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import json
import os

from spdx_tools.spdx3.payload import Payload
# from spdx_tools.spdx3.writer.json_ld.json_ld_converter import convert_payload_to_json_ld_list_of_elements

class JsonLDParser:
    logger: Logger

    def __init__(self):
        self.logger = Logger()

    def parse(self, file_name: str) -> Document:
        with open(file_name, "r") as file:
            pass
