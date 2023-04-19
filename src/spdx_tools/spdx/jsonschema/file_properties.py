# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from enum import auto

from spdx_tools.spdx.jsonschema.json_property import JsonProperty


class FileProperty(JsonProperty):
    SPDX_ID = auto()
    ANNOTATIONS = auto()
    ARTIFACT_OFS = auto()
    ATTRIBUTION_TEXTS = auto()
    CHECKSUMS = auto()
    COMMENT = auto()
    COPYRIGHT_TEXT = auto()
    FILE_CONTRIBUTORS = auto()
    FILE_DEPENDENCIES = auto()
    FILE_NAME = auto()
    FILE_TYPES = auto()
    LICENSE_COMMENTS = auto()
    LICENSE_CONCLUDED = auto()
    LICENSE_INFO_IN_FILES = auto()
    NOTICE_TEXT = auto()
