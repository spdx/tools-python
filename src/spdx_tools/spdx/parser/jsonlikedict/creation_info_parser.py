# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime

from beartype.typing import Dict, List, Optional

from spdx_tools.spdx.datetime_conversions import datetime_from_str
from spdx_tools.spdx.model import Actor, Checksum, CreationInfo, ExternalDocumentRef, Version
from spdx_tools.spdx.parser.actor_parser import ActorParser
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.jsonlikedict.checksum_parser import ChecksumParser
from spdx_tools.spdx.parser.jsonlikedict.dict_parsing_functions import parse_field_or_log_error
from spdx_tools.spdx.parser.logger import Logger
from spdx_tools.spdx.parser.parsing_functions import (
    construct_or_raise_parsing_error,
    raise_parsing_error_if_logger_has_messages,
)


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

        creators: List[Actor] = parse_field_or_log_error(
            logger, creation_info_dict.get("creators"), self.actor_parser.parse_actor, field_is_list=True
        )

        created: Optional[datetime] = parse_field_or_log_error(
            logger, creation_info_dict.get("created"), datetime_from_str
        )

        creator_comment: Optional[str] = creation_info_dict.get("comment")
        data_license: Optional[str] = doc_dict.get("dataLicense")

        external_document_refs: List[ExternalDocumentRef] = parse_field_or_log_error(
            logger, doc_dict.get("externalDocumentRefs"), self.parse_external_document_refs
        )
        license_list_version: Optional[Version] = parse_field_or_log_error(
            logger, creation_info_dict.get("licenseListVersion"), self.parse_version
        )
        document_comment: Optional[str] = doc_dict.get("comment")
        raise_parsing_error_if_logger_has_messages(logger, "Document")

        creation_info = construct_or_raise_parsing_error(
            CreationInfo,
            dict(
                spdx_version=spdx_version,
                spdx_id=spdx_id,
                name=name,
                document_namespace=document_namespace,
                creators=creators,
                created=created,
                license_list_version=license_list_version,
                document_comment=document_comment,
                creator_comment=creator_comment,
                data_license=data_license,
                external_document_refs=external_document_refs,
            ),
        )

        return creation_info

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
            external_document_ref: ExternalDocumentRef = parse_field_or_log_error(
                logger, external_document_ref_dict, self.parse_external_document_ref
            )

            external_document_refs.append(external_document_ref)

        raise_parsing_error_if_logger_has_messages(logger)
        return external_document_refs

    def parse_external_document_ref(self, external_document_ref_dict: Dict) -> ExternalDocumentRef:
        logger = Logger()
        checksum: Optional[Checksum] = parse_field_or_log_error(
            logger, external_document_ref_dict.get("checksum"), self.checksum_parser.parse_checksum
        )

        external_document_id: Optional[str] = external_document_ref_dict.get("externalDocumentId")
        document_uri: Optional[str] = external_document_ref_dict.get("spdxDocument")
        raise_parsing_error_if_logger_has_messages(logger, "ExternalDocumentRef")
        external_document_ref: ExternalDocumentRef = construct_or_raise_parsing_error(
            ExternalDocumentRef,
            dict(document_ref_id=external_document_id, checksum=checksum, document_uri=document_uri),
        )

        return external_document_ref
