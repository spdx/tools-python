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
from datetime import datetime
from typing import Dict, Optional, List

from src.model.actor import Actor
from src.model.checksum import Checksum
from src.model.document import CreationInfo
from src.model.external_document_ref import ExternalDocumentRef
from src.model.version import Version
from src.parser.error import SPDXParsingError
from src.parser.json.actor_parser import ActorParser
from src.parser.json.checksum_parser import ChecksumParser
from src.parser.json.dict_parsing_functions import append_parsed_field_or_log_error, datetime_from_str, \
    raise_parsing_error_if_logger_has_messages, construct_or_raise_parsing_error, parse_field_or_log_error
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
        logger = Logger()
        spdx_version: str = doc_dict.get("spdxVersion")
        spdx_id: str = doc_dict.get("SPDXID")
        name: str = doc_dict.get("name")
        document_namespace: str = doc_dict.get("documentNamespace")
        creation_info_dict: Dict = doc_dict.get("creationInfo")

        # There are nested required properties. If creationInfo is not set, we cannot continue parsing.
        if creation_info_dict is None:
            logger.append("CreationInfo does not exist.")
            raise SPDXParsingError([f"Error while parsing doc {name}: {logger.get_messages()}"])

        list_of_creators: List[str] = creation_info_dict.get("creators")
        creators: List[Actor] = parse_field_or_log_error(logger=logger, field=list_of_creators,
                                                         parsing_method=self.parse_creators, default=[])

        created: Optional[datetime] = parse_field_or_log_error(logger=logger, field=creation_info_dict.get(
            "created"), parsing_method=datetime_from_str)

        creator_comment: Optional[str] = creation_info_dict.get("comment")
        data_license: str = doc_dict.get("dataLicense")

        external_document_refs: List[ExternalDocumentRef] = parse_field_or_log_error(
            logger=logger, field=doc_dict.get("externalDocumentRefs"),
            parsing_method=self.parse_external_document_refs, optional=True)
        license_list_version: Optional[Version] = parse_field_or_log_error(logger=logger,
                                                                           field=creation_info_dict.get(
                                                                                   "licenseListVersion"),
                                                                           parsing_method=self.parse_version,
                                                                           optional=True)
        document_comment: Optional[str] = doc_dict.get("comment")
        raise_parsing_error_if_logger_has_messages(logger, f"Document: {name}")

        creation_info = construct_or_raise_parsing_error(CreationInfo,
                                                         dict(spdx_version=spdx_version, spdx_id=spdx_id, name=name,
                                                              document_namespace=document_namespace,
                                                              creators=creators, created=created,
                                                              license_list_version=license_list_version,
                                                              document_comment=document_comment, creator_comment=creator_comment,
                                                              data_license=data_license,
                                                              external_document_refs=external_document_refs))

        return creation_info

    def parse_creators(self, creators_list_from_dict: List[str]) -> List[Actor]:
        logger = Logger()
        creators_list = []
        for creator_dict in creators_list_from_dict:
            creators_list = append_parsed_field_or_log_error(list_to_append_to=creators_list, logger=logger, field=creator_dict,
                                                             method_to_parse=self.actor_parser.parse_actor_or_no_assertion)

        raise_parsing_error_if_logger_has_messages(logger)
        return creators_list

    @staticmethod
    def parse_version(version_str: str) -> Version:
        try:
            return Version.from_string(version_str)
        except ValueError as err:
            raise SPDXParsingError([f"Error while parsing version {version_str}: {err.args[0]}"])

    def parse_external_document_refs(self, external_document_refs_dict: List[Dict]) -> List[ExternalDocumentRef]:
        logger = Logger()
        external_document_refs = []
        for external_ref_dict in external_document_refs_dict:
            external_doc_ref: ExternalDocumentRef = parse_field_or_log_error(logger=logger, field=external_ref_dict,
                                                                             parsing_method=self.parse_external_doc_ref,
                                                                             optional=True)

            external_document_refs.append(external_doc_ref)

        raise_parsing_error_if_logger_has_messages(logger)
        return external_document_refs

    def parse_external_doc_ref(self, external_doc_ref_dict: Dict) -> ExternalDocumentRef:
        logger = Logger()
        checksum: Optional[Checksum] = parse_field_or_log_error(logger=logger, field=external_doc_ref_dict.get(
            "checksum"), parsing_method=self.checksum_parser.parse_checksum)

        external_document_id: str = external_doc_ref_dict.get("externalDocumentId")
        spdx_document: str = external_doc_ref_dict.get("spdxDocument")
        raise_parsing_error_if_logger_has_messages(logger, "ExternalDocRef")
        external_doc_ref = construct_or_raise_parsing_error(ExternalDocumentRef,
                                                            dict(document_ref_id=external_document_id,
                                                                 checksum=checksum, document_uri=spdx_document))

        return external_doc_ref
