# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

import sys

MISSING_CONVERSION_REASONS = {0: "missing conversion rule", 1: "missing implementation"}


def print_missing_conversion(field: str, reason, additional_information: str = ""):
    print(f"{field} not converted: {MISSING_CONVERSION_REASONS[reason]} {additional_information}", file=sys.stderr)
