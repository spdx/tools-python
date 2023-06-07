# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import List


class Logger:
    messages: List[str]

    def __init__(self):
        self.messages = []

    def append(self, message: str):
        self.messages.append(message)

    def extend(self, messages_to_append: List[str]):
        self.messages.extend(messages_to_append)

    def has_messages(self):
        return bool(self.messages)

    def get_messages(self):
        return list(self.messages)
