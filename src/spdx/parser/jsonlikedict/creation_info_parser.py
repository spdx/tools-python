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

from spdx.model.actor import Actor
from spdx.model.checksum import Checksum
from spdx.model.document import CreationInfo
from spdx.model.external_document_ref import ExternalDocumentRef
from spdx.model.version import Version
from spdx.parser.error import SPDXParsingError
from spdx.parser.actor_parser import ActorParser
from spdx.parser.jsonlikedict.checksum_parser import ChecksumParser
from spdx.parser.jsonlikedict.dict_parsing_functions import append_parsed_field_or_log_error, \
    parse_field_or_log_error, \
    parse_field_or_no_assertion
from spdx.parser.parsing_functions import construct_or_raise_parsing_error, raise_parsing_error_if_logger_has_messages
from spdx.datetime_conversions import datetime_from_str
from spdx.parser.logger import Logger


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
        spdx_version: Optional[str] = doc_dict.get("spdxVersion")
        spdx_id: Optional[str] = doc_dict.get("SPDXID")
        name: Optional[str] = doc_dict.get("name")
        document_namespace: Optional[str] = doc_dict.get("documentNamespace")
        creation_info_dict: Optional[Dict] = doc_dict.get("creationInfo")

        # There are nested required properties. If creationInfo is not set, we cannot continue parsing.
        if creation_info_dict is None:
            logger.append("CreationInfo does not exist.")
            raise SPDXParsingError([f"Error while parsing document {name}: {logger.get_messages()}"])

        creators: List[Actor] = parse_field_or_log_error(logger, creation_info_dict.get("creators"),
                                                         self.parse_creators)

        created: Optional[datetime] = parse_field_or_log_error(logger, creation_info_dict.get("created"),
                                                               datetime_from_str)

        creator_comment: Optional[str] = creation_info_dict.get("comment")
        data_license: Optional[str] = doc_dict.get("dataLicense")

        external_document_refs: List[ExternalDocumentRef] = parse_field_or_log_error(logger, doc_dict.get(
            "externalDocumentRefs"), self.parse_external_document_refs)
        license_list_version: Optional[Version] = parse_field_or_log_error(logger,
                                                                           creation_info_dict.get("licenseListVersion"),
                                                                           self.parse_version)
        document_comment: Optional[str] = doc_dict.get("comment")
        raise_parsing_error_if_logger_has_messages(logger, "Document")

        creation_info = construct_or_raise_parsing_error(CreationInfo,
                                                         dict(spdx_version=spdx_version, spdx_id=spdx_id, name=name,
                                                              document_namespace=document_namespace,
                                                              creators=creators, created=created,
                                                              license_list_version=license_list_version,
                                                              document_comment=document_comment,
                                                              creator_comment=creator_comment,
                                                              data_license=data_license,
                                                              external_document_refs=external_document_refs))

        return creation_info

    def parse_creators(self, creators_list_from_dict: List[str]) -> List[Actor]:
        logger = Logger()
        creators = []
        for creator_str in creators_list_from_dict:
            creators = append_parsed_field_or_log_error(logger, creators, creator_str, lambda x: parse_field_or_no_assertion(x, self.actor_parser.parse_actor))

        raise_parsing_error_if_logger_has_messages(logger)
        return creators

    @staticmethod
    def parse_version(version_str: str) -> Version:
        try:
            return Version.from_string(version_str)
        except ValueError as err:
            raise SPDXParsingError([f"Error while parsing version {version_str}: {err.args[0]}"])

    def parse_external_document_refs(self, external_document_ref_dicts: List[Dict]) -> List[ExternalDocumentRef]:
        logger = Logger()
        external_document_refs = []
        for external_document_ref_dict in external_document_ref_dicts:
            external_document_ref: ExternalDocumentRef = parse_field_or_log_error(logger, external_document_ref_dict,
                                                                                  self.parse_external_document_ref)

            external_document_refs.append(external_document_ref)

        raise_parsing_error_if_logger_has_messages(logger)
        return external_document_refs

    def parse_external_document_ref(self, external_document_ref_dict: Dict) -> ExternalDocumentRef:
        logger = Logger()
        checksum: Optional[Checksum] = parse_field_or_log_error(logger, external_document_ref_dict.get("checksum"),
                                                                self.checksum_parser.parse_checksum)

        external_document_id: Optional[str] = external_document_ref_dict.get("externalDocumentId")
        document_uri: Optional[str] = external_document_ref_dict.get("spdxDocument")
        raise_parsing_error_if_logger_has_messages(logger, "ExternalDocumentRef")
        external_document_ref: ExternalDocumentRef = construct_or_raise_parsing_error(ExternalDocumentRef,
                                                                                 dict(
                                                                                     document_ref_id=external_document_id,
                                                                                     checksum=checksum,
                                                                                     document_uri=document_uri))

        return external_document_ref
