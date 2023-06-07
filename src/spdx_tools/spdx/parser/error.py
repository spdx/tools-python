# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import List


class SPDXParsingError(Exception):
    messages: List[str]

    def __init__(self, messages: List[str]):
        self.messages = messages

    def get_messages(self):
        return list(self.messages)
