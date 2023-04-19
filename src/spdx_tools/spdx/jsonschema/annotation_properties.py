# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from enum import auto

from spdx_tools.spdx.jsonschema.json_property import JsonProperty


class AnnotationProperty(JsonProperty):
    ANNOTATION_DATE = auto()
    ANNOTATION_TYPE = auto()
    ANNOTATOR = auto()
    COMMENT = auto()
