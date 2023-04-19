# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from enum import auto

from spdx_tools.spdx.jsonschema.json_property import JsonProperty


class DocumentProperty(JsonProperty):
    SPDX_ID = auto()
    ANNOTATIONS = auto()
    COMMENT = auto()
    CREATION_INFO = auto()
    DATA_LICENSE = auto()
    EXTERNAL_DOCUMENT_REFS = auto()
    HAS_EXTRACTED_LICENSING_INFOS = auto()
    NAME = auto()
    SPDX_VERSION = auto()
    DOCUMENT_NAMESPACE = auto()
    PACKAGES = auto()
    FILES = auto()
    SNIPPETS = auto()
    RELATIONSHIPS = auto()
