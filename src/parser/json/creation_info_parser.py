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
from typing import Dict, Optional, List

from src.model.actor import Actor
from src.model.document import CreationInfo
from src.model.external_document_ref import ExternalDocumentRef
from src.model.typing.constructor_type_errors import ConstructorTypeErrors
from src.model.version import Version
from src.parser.error import SPDXParsingError
from src.parser.json.actor_parser import ActorParser
from src.parser.json.checksum_parser import ChecksumParser
from src.parser.json.dict_parsing_functions import datetime_from_str, parse_optional_field
from src.parser.logger import Logger


class CreationInfoParser:
    logger: Logger
    actor_parser: ActorParser
    checksum_parser: ChecksumParser

    def __init__(self):
        self.logger = Logger()
        self.actor_parser = ActorParser()
        self.checksum_parser = ChecksumParser()

    def parse_creation_info(self, doc_dict: Dict) -> CreationInfo:
        spdx_version: str = doc_dict.get("spdxVersion")
        spdx_id: str = doc_dict.get("SPDXID")
        name: str = doc_dict.get("name")
        document_namespace: str = doc_dict.get("documentNamespace")
        creation_info_dict: Dict = doc_dict.get("creationInfo")

        # There are nested required properties. If creationInfo is not set, we cannot continue parsing.
        if creation_info_dict is None:
            self.logger.append("CreationInfo is not valid.")
            raise SPDXParsingError(self.logger.get_messages())

        list_of_creators = creation_info_dict.get("creators")
        creators = self.parse_creators(list_of_creators)

        try:
            created = datetime_from_str(creation_info_dict.get("created"))
        except ValueError:
            self.logger.append("Error while parsing created")
            created = None

        creator_comment = creation_info_dict.get("comment")
        data_license = doc_dict.get("dataLicense")
        external_document_refs = parse_optional_field(doc_dict.get("externalDocumentRefs"), self.parse_external_document_refs)
        license_list_version = parse_optional_field(creation_info_dict.get("licenseListVersion"), self.parse_version)

        document_comment = doc_dict.get("comment")
        if self.logger.has_messages():
            raise SPDXParsingError(self.logger.get_messages())
        try:
            creation_info = CreationInfo(spdx_version=spdx_version, spdx_id=spdx_id, name=name,
                                         document_namespace=document_namespace, creators=creators, created=created,
                                         license_list_version=license_list_version, document_comment=document_comment,
                                         creator_comment=creator_comment, data_license=data_license,
                                         external_document_refs=external_document_refs)
        except ConstructorTypeErrors as err:
            self.logger.append_all(err.get_messages())
            raise SPDXParsingError(self.logger.get_messages())

        return creation_info

    def parse_version(self, version_str: str) -> Optional[Version]:
        try:
            return Version.from_string(version_str)
        except ValueError as err:
            self.logger.append(err.args[0])
            return None

    def parse_creators(self, creators_dict_list: List[str]) -> List[Actor]:
        creators_list = []
        for creator_dict in creators_dict_list:
            try:
                creator = self.actor_parser.parse_actor_or_no_assert(creator_dict)
                creators_list.append(creator)
            except SPDXParsingError as err:
                self.logger.append_all(err.get_messages())
        return creators_list

    def parse_external_document_refs(self, external_document_refs_dict: List[Dict]) -> List[ExternalDocumentRef]:
        external_document_refs = []
        for external_ref_dict in external_document_refs_dict:
            try:
                external_doc_ref = self.parse_external_doc_ref(external_ref_dict)
                external_document_refs.append(external_doc_ref)
            except SPDXParsingError as err:
                self.logger.append_all(err.get_messages())
        return external_document_refs
    def parse_external_doc_ref(self, external_doc_ref_dict: Dict) -> ExternalDocumentRef:
        checksum = self.checksum_parser.parse_checksum(external_doc_ref_dict.get("checksum"))
        external_document_id = external_doc_ref_dict.get("externalDocumentId")
        spdx_document = external_doc_ref_dict.get("spdxDocument")
        try:
            external_doc_ref = ExternalDocumentRef(document_ref_id=external_document_id, document_uri=spdx_document, checksum=checksum)
        except ConstructorTypeErrors as err:
            raise SPDXParsingError(err.get_messages())

        return external_doc_ref

