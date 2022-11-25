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
from typing import Dict, Tuple

from src.model.document import CreationInfo
from src.parser.logger import Logger


class CreationInfoParser:
    logger: Logger

    def __init__(self, logger: Logger):
        self.logger = logger

    def parse_creation_info(self, creation_info_dict: Dict) -> CreationInfo:
        creators = creation_info_dict.get("creators")
        created = creation_info_dict.get("created")
        creation_info = CreationInfo(creators, created)
        if "comment" in creation_info_dict:
            creation_info.comment = creation_info_dict.get("comment")

        if "licenseListVersion" in creation_info_dict:
            creation_info.license_list_version = creation_info_dict.get("licenseListVersion")

        return creation_info

    def parse(self, doc_dict: Dict) -> Tuple[str, str, str, str, CreationInfo]:
        spdx_version = doc_dict.get("spdxVersion")
        spdx_id = doc_dict.get("SPDXID")
        name = doc_dict.get("name")
        document_namespace = doc_dict.get("documentNamespace")
        creation_info = self.parse_creation_info(doc_dict.get("creationInfo"))

        return spdx_version, spdx_id, name, document_namespace, creation_info
