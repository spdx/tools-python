# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from enum import auto

from spdx_tools.spdx.jsonschema.json_property import JsonProperty


class SnippetProperty(JsonProperty):
    SPDX_ID = auto()
    ANNOTATIONS = auto()
    ATTRIBUTION_TEXTS = auto()
    COMMENT = auto()
    COPYRIGHT_TEXT = auto()
    LICENSE_COMMENTS = auto()
    LICENSE_CONCLUDED = auto()
    LICENSE_INFO_IN_SNIPPETS = auto()
    NAME = auto()
    RANGES = auto()
    SNIPPET_FROM_FILE = auto()
