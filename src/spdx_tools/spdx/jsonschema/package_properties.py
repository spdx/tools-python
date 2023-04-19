# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from enum import auto

from spdx_tools.spdx.jsonschema.json_property import JsonProperty


class PackageProperty(JsonProperty):
    SPDX_ID = auto()
    ANNOTATIONS = auto()
    ATTRIBUTION_TEXTS = auto()
    BUILT_DATE = auto()
    CHECKSUMS = auto()
    COMMENT = auto()
    COPYRIGHT_TEXT = auto()
    DESCRIPTION = auto()
    DOWNLOAD_LOCATION = auto()
    EXTERNAL_REFS = auto()
    FILES_ANALYZED = auto()
    HOMEPAGE = auto()
    LICENSE_COMMENTS = auto()
    LICENSE_CONCLUDED = auto()
    LICENSE_DECLARED = auto()
    LICENSE_INFO_FROM_FILES = auto()
    NAME = auto()
    ORIGINATOR = auto()
    PACKAGE_FILE_NAME = auto()
    PACKAGE_VERIFICATION_CODE = auto()
    PRIMARY_PACKAGE_PURPOSE = auto()
    RELEASE_DATE = auto()
    SOURCE_INFO = auto()
    SUMMARY = auto()
    SUPPLIER = auto()
    VALID_UNTIL_DATE = auto()
    VERSION_INFO = auto()
