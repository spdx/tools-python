# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

SPDX_NO_ASSERTION_STRING = "NOASSERTION"


class SpdxNoAssertion:
    """
    Represents the SPDX NOASSERTION value.
    """

    def __str__(self):
        return SPDX_NO_ASSERTION_STRING

    def __repr__(self):
        return SPDX_NO_ASSERTION_STRING

    def __eq__(self, other):
        return isinstance(other, SpdxNoAssertion)
