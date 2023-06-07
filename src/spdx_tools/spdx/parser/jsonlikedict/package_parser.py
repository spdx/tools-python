# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime

from beartype.typing import Dict, List, Optional, Union
from license_expression import LicenseExpression

from spdx_tools.spdx.datetime_conversions import datetime_from_str
from spdx_tools.spdx.model import (
    Actor,
    ExternalPackageRef,
    ExternalPackageRefCategory,
    Package,
    PackagePurpose,
    PackageVerificationCode,
    SpdxNoAssertion,
    SpdxNone,
)
from spdx_tools.spdx.parser.actor_parser import ActorParser
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.jsonlikedict.checksum_parser import ChecksumParser
from spdx_tools.spdx.parser.jsonlikedict.dict_parsing_functions import (
    append_parsed_field_or_log_error,
    json_str_to_enum_name,
    parse_field_or_log_error,
    parse_field_or_no_assertion,
    parse_field_or_no_assertion_or_none,
)
from spdx_tools.spdx.parser.jsonlikedict.license_expression_parser import LicenseExpressionParser
from spdx_tools.spdx.parser.logger import Logger
from spdx_tools.spdx.parser.parsing_functions import (
    construct_or_raise_parsing_error,
    raise_parsing_error_if_logger_has_messages,
)


class PackageParser:
    logger: Logger
    actor_parser: ActorParser
    checksum_parser: ChecksumParser
    license_expression_parser: LicenseExpressionParser

    def __init__(self):
        self.actor_parser = ActorParser()
        self.checksum_parser = ChecksumParser()
        self.license_expression_parser = LicenseExpressionParser()
        self.logger = Logger()

    def parse_package(self, package_dict: Dict) -> Package:
        logger = Logger()
        name: Optional[str] = package_dict.get("name")
        spdx_id: Optional[str] = package_dict.get("SPDXID")
        attribution_texts: List[str] = package_dict.get("attributionTexts", [])

        built_date: Optional[datetime] = parse_field_or_log_error(
            logger, package_dict.get("builtDate"), datetime_from_str
        )

        checksums = parse_field_or_log_error(
            logger, package_dict.get("checksums"), self.checksum_parser.parse_checksum, field_is_list=True
        )
        comment: Optional[str] = package_dict.get("comment")
        copyright_text: Optional[Union[str, SpdxNoAssertion, SpdxNone]] = parse_field_or_no_assertion_or_none(
            package_dict.get("copyrightText")
        )
        description: Optional[str] = package_dict.get("description")
        download_location: Optional[Union[str, SpdxNoAssertion, SpdxNone]] = parse_field_or_no_assertion_or_none(
            package_dict.get("downloadLocation")
        )

        external_refs: List[ExternalPackageRef] = parse_field_or_log_error(
            logger, package_dict.get("externalRefs"), self.parse_external_refs
        )

        files_analyzed: Optional[Union[bool, str]] = package_dict.get("filesAnalyzed")

        if files_analyzed is None:  # default value is True
            files_analyzed = True
        elif isinstance(files_analyzed, str):  # XML does not support boolean typed values
            if files_analyzed.lower() == "true":
                files_analyzed = True
            elif files_analyzed.lower() == "false":
                files_analyzed = False

        homepage: Optional[Union[str, SpdxNoAssertion, SpdxNone]] = parse_field_or_no_assertion_or_none(
            package_dict.get("homepage")
        )
        license_comments: Optional[str] = package_dict.get("licenseComments")
        license_concluded = parse_field_or_log_error(
            logger, package_dict.get("licenseConcluded"), self.license_expression_parser.parse_license_expression
        )

        license_declared: Optional[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]] = parse_field_or_log_error(
            logger, package_dict.get("licenseDeclared"), self.license_expression_parser.parse_license_expression
        )

        license_info_from_file: List[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]] = parse_field_or_log_error(
            logger,
            package_dict.get("licenseInfoFromFiles"),
            self.license_expression_parser.parse_license_expression,
            field_is_list=True,
        )
        originator: Optional[Union[Actor, SpdxNoAssertion]] = parse_field_or_log_error(
            logger,
            package_dict.get("originator"),
            lambda x: parse_field_or_no_assertion(x, self.actor_parser.parse_actor),
        )
        package_file_name: Optional[str] = package_dict.get("packageFileName")

        package_verification_code: Optional[PackageVerificationCode] = parse_field_or_log_error(
            logger, package_dict.get("packageVerificationCode"), self.parse_package_verification_code
        )
        primary_package_purpose: Optional[PackagePurpose] = parse_field_or_log_error(
            logger, package_dict.get("primaryPackagePurpose"), self.parse_primary_package_purpose
        )

        release_date: Optional[datetime] = parse_field_or_log_error(
            logger, package_dict.get("releaseDate"), datetime_from_str
        )
        source_info: Optional[str] = package_dict.get("sourceInfo")
        summary: Optional[str] = package_dict.get("summary")
        supplier: Optional[Union[Actor, SpdxNoAssertion]] = parse_field_or_log_error(
            logger,
            package_dict.get("supplier"),
            lambda x: parse_field_or_no_assertion(x, self.actor_parser.parse_actor),
        )
        valid_until_date: Optional[datetime] = parse_field_or_log_error(
            logger, package_dict.get("validUntilDate"), datetime_from_str
        )

        version_info: Optional[str] = package_dict.get("versionInfo")
        raise_parsing_error_if_logger_has_messages(logger, "Package")

        package = construct_or_raise_parsing_error(
            Package,
            dict(
                spdx_id=spdx_id,
                name=name,
                download_location=download_location,
                version=version_info,
                file_name=package_file_name,
                supplier=supplier,
                originator=originator,
                files_analyzed=files_analyzed,
                verification_code=package_verification_code,
                checksums=checksums,
                homepage=homepage,
                source_info=source_info,
                license_concluded=license_concluded,
                license_info_from_files=license_info_from_file,
                license_declared=license_declared,
                license_comment=license_comments,
                copyright_text=copyright_text,
                summary=summary,
                description=description,
                comment=comment,
                external_references=external_refs,
                attribution_texts=attribution_texts,
                primary_package_purpose=primary_package_purpose,
                release_date=release_date,
                built_date=built_date,
                valid_until_date=valid_until_date,
            ),
        )

        return package

    def parse_external_refs(self, external_ref_dicts: List[Dict]) -> List[ExternalPackageRef]:
        external_refs = []
        for external_ref_dict in external_ref_dicts:
            external_refs = append_parsed_field_or_log_error(
                self.logger, external_refs, external_ref_dict, self.parse_external_ref
            )
        return external_refs

    def parse_external_ref(self, external_ref_dict: Dict) -> ExternalPackageRef:
        logger = Logger()
        ref_category = parse_field_or_log_error(
            logger, external_ref_dict.get("referenceCategory"), self.parse_external_ref_category
        )
        ref_locator: Optional[str] = external_ref_dict.get("referenceLocator")
        ref_type: Optional[str] = external_ref_dict.get("referenceType")
        comment: Optional[str] = external_ref_dict.get("comment")
        raise_parsing_error_if_logger_has_messages(logger, "ExternalPackageRef")
        external_ref = construct_or_raise_parsing_error(
            ExternalPackageRef,
            dict(category=ref_category, reference_type=ref_type, locator=ref_locator, comment=comment),
        )

        return external_ref

    @staticmethod
    def parse_external_ref_category(external_ref_category_str: str) -> ExternalPackageRefCategory:
        try:
            external_ref_category = ExternalPackageRefCategory[json_str_to_enum_name(external_ref_category_str)]
        except KeyError:
            raise SPDXParsingError([f"Invalid ExternalPackageRefCategory: {external_ref_category_str}"])

        return external_ref_category

    @staticmethod
    def parse_package_verification_code(verification_code_dict: Dict) -> PackageVerificationCode:
        excluded_files: List[str] = verification_code_dict.get("packageVerificationCodeExcludedFiles", [])
        verification_code_value: Optional[str] = verification_code_dict.get("packageVerificationCodeValue")

        package_verification_code = construct_or_raise_parsing_error(
            PackageVerificationCode, dict(value=verification_code_value, excluded_files=excluded_files)
        )

        return package_verification_code

    @staticmethod
    def parse_primary_package_purpose(primary_package_purpose: str) -> PackagePurpose:
        try:
            return PackagePurpose[json_str_to_enum_name(primary_package_purpose)]
        except KeyError:
            raise SPDXParsingError([f"Invalid PrimaryPackagePurpose: {primary_package_purpose}"])
