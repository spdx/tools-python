# Copyright (c) 2022 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from enum import auto

from spdx.jsonschema.json_property import JsonProperty


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
    HAS_FILES = auto()
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
