# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from dataclasses import dataclass


def dataclass_with_properties(cls):
    # placeholder decorator until we figure out how to do run-time type checking more performant
    return dataclass(cls)
