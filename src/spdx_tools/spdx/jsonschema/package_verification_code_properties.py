# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from enum import auto

from spdx_tools.spdx.jsonschema.json_property import JsonProperty


class PackageVerificationCodeProperty(JsonProperty):
    PACKAGE_VERIFICATION_CODE_EXCLUDED_FILES = auto()
    PACKAGE_VERIFICATION_CODE_VALUE = auto()
