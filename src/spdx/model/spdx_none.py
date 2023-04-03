# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

SPDX_NONE_STRING = "NONE"


class SpdxNone:
    """
    Represents the SPDX NONE value.
    """

    def __str__(self):
        return SPDX_NONE_STRING

    def __repr__(self):
        return SPDX_NONE_STRING

    def __eq__(self, other):
        return isinstance(other, SpdxNone)
