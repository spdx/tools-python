# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import List


class ConstructorTypeErrors(TypeError):
    """
    Helper class that holds a list of error messages. Intended to capture all TypeErrors encountered during a
    constructor call, instead of raising only the first one.
    """

    messages: List[str]

    def __init__(self, messages: List[str]):
        self.messages = messages

    def get_messages(self):
        return list(self.messages)
