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
from typing import Dict, List, Optional, Union

from src.model.actor import Actor
from src.model.license_expression import LicenseExpression
from src.model.package import Package, ExternalPackageRef, PackageVerificationCode, PackagePurpose, \
    ExternalPackageRefCategory
from src.model.spdx_no_assertion import SpdxNoAssertion
from src.model.spdx_none import SpdxNone
from src.parser.error import SPDXParsingError
from src.parser.json.actor_parser import ActorParser
from src.parser.json.checksum_parser import ChecksumParser
from src.parser.json.dict_parsing_functions import append_parsed_field_or_log_error, datetime_from_str, \
    raise_parsing_error_if_logger_has_messages, json_str_to_enum_name, construct_or_raise_parsing_error, \
    parse_field_or_log_error
from src.parser.json.license_expression_parser import LicenseExpressionParser
from src.parser.logger import Logger


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

    def parse_packages(self, packages_dict_list: List[Dict]) -> List[Package]:
        packages_list = []
        for package_dict in packages_dict_list:
            packages_list = append_parsed_field_or_log_error(logger=self.logger, list_to_append_to=packages_list,
                                                             field=package_dict, method_to_parse=self.parse_package)

        raise_parsing_error_if_logger_has_messages(self.logger)

        return packages_list

    def parse_package(self, package_dict: Dict) -> Package:
        logger = Logger()
        name: str = package_dict.get("name")
        spdx_id: str = package_dict.get("SPDXID")
        attribution_texts: List[str] = package_dict.get("attributionTexts")

        built_date: Optional[datetime] = parse_field_or_log_error(logger=logger, field=package_dict.get("builtDate"),
                                                                  parsing_method=datetime_from_str, optional=True)

        checksums = parse_field_or_log_error(logger=logger, field=package_dict.get("checksums"),
                                             parsing_method=self.checksum_parser.parse_checksums, optional=True)
        comment: Optional[str] = package_dict.get("comment")
        copyright_text: Optional[str] = package_dict.get("copyrightText")
        description: Optional[str] = package_dict.get("description")
        download_location: Union[str, SpdxNoAssertion, SpdxNone] = self.parse_download_location(
            package_dict.get("downloadLocation"))

        external_refs: List[ExternalPackageRef] = parse_field_or_log_error(logger=logger,
                                                                           field=package_dict.get("externalRefs"),
                                                                           parsing_method=self.parse_external_refs,
                                                                           optional=True)

        files_analyzed: Optional[bool] = parse_field_or_log_error(logger=logger,
                                                                  field=package_dict.get("filesAnalyzed"),
                                                                  parsing_method=lambda x: x, optional=True,
                                                                  default=True)
        homepage: Optional[str] = package_dict.get("homepage")
        license_comments: Optional[str] = package_dict.get("licenseComments")
        license_concluded = parse_field_or_log_error(logger=logger, field=package_dict.get("licenseConcluded"),
                                                     parsing_method=self.license_expression_parser.parse_license_expression,
                                                     default=None, optional=True)

        license_declared: Optional[Union[LicenseExpression, SpdxNoAssertion, SpdxNone]] = parse_field_or_log_error(
            logger=logger, field=package_dict.get("licenseDeclared"),
            parsing_method=self.license_expression_parser.parse_license_expression, optional=True)

        license_info_from_file: Optional[
            Union[List[LicenseExpression], SpdxNoAssertion, SpdxNone]] = parse_field_or_log_error(
            logger=logger, field=package_dict.get("licenseInfoFromFiles"),
            parsing_method=self.license_expression_parser.parse_license_expression, optional=True)

        originator: Optional[Union[Actor, SpdxNoAssertion]] = parse_field_or_log_error(
            logger=logger, field=package_dict.get("originator"),
            parsing_method=self.actor_parser.parse_actor_or_no_assertion, optional=True)

        package_file_name: Optional[str] = package_dict.get("packageFileName")

        package_verification_code: Optional[
            PackageVerificationCode] = parse_field_or_log_error(logger=logger,
                                                                field=package_dict.get("packageVerificationCode"),
                                                                parsing_method=self.parse_package_verification_code,
                                                                optional=True)
        primary_package_purpose: Optional[PackagePurpose] = parse_field_or_log_error(
            logger=logger, field=package_dict.get("primaryPackagePurpose"),
            parsing_method=self.parse_primary_package_purpose, optional=True)

        release_date: Optional[datetime] = parse_field_or_log_error(logger=logger,
                                                                    field=package_dict.get("releaseDate"),
                                                                    parsing_method=datetime_from_str, optional=True)

        source_info: Optional[str] = package_dict.get("sourceInfo")
        summary: Optional[str] = package_dict.get("summary")
        supplier: Optional[Union[Actor, SpdxNoAssertion]] = parse_field_or_log_error(
            logger=logger, field=package_dict.get("supplier"),
            parsing_method=self.actor_parser.parse_actor_or_no_assertion, optional=True)

        valid_until_date: Optional[datetime] = parse_field_or_log_error(logger=logger,
                                                                        field=package_dict.get("validUntilDate"),
                                                                        parsing_method=datetime_from_str,
                                                                        optional=True)

        version_info: Optional[str] = package_dict.get("versionInfo")
        raise_parsing_error_if_logger_has_messages(logger, f"Package {name}")

        package = construct_or_raise_parsing_error(Package,
                                                   dict(spdx_id=spdx_id, name=name, download_location=download_location,
                                                        version=version_info, file_name=package_file_name,
                                                        supplier=supplier, originator=originator,
                                                        files_analyzed=files_analyzed,
                                                        verification_code=package_verification_code,
                                                        checksums=checksums, homepage=homepage, source_info=source_info,
                                                        license_concluded=license_concluded,
                                                        license_info_from_files=license_info_from_file,
                                                        license_declared=license_declared,
                                                        license_comment=license_comments,
                                                        copyright_text=copyright_text, summary=summary,
                                                        description=description, comment=comment,
                                                        external_references=external_refs,
                                                        attribution_texts=attribution_texts,
                                                        primary_package_purpose=primary_package_purpose,
                                                        release_date=release_date, built_date=built_date,
                                                        valid_until_date=valid_until_date))

        return package

    def parse_external_refs(self, external_ref_dicts: List[Dict]) -> List[ExternalPackageRef]:
        external_refs = []
        for external_ref_dict in external_ref_dicts:
            external_refs = append_parsed_field_or_log_error(logger=self.logger, list_to_append_to=external_refs,
                                                             field=external_ref_dict, method_to_parse=self.parse_external_ref)

        return external_refs

    def parse_external_ref(self, external_ref_dict: Dict) -> ExternalPackageRef:
        logger = Logger()
        ref_category = parse_field_or_log_error(logger=logger, field=external_ref_dict.get("referenceCategory"),
                                                parsing_method=self.parse_external_ref_category)
        ref_locator = external_ref_dict.get("referenceLocator")
        ref_type = external_ref_dict.get("referenceType")
        comment = external_ref_dict.get("comment")
        raise_parsing_error_if_logger_has_messages(logger, "external  ref")
        external_ref = construct_or_raise_parsing_error(ExternalPackageRef,
                                                        dict(category=ref_category, reference_type=ref_type,
                                                             locator=ref_locator, comment=comment))

        return external_ref

    @staticmethod
    def parse_external_ref_category(external_ref_category_str: str) -> ExternalPackageRefCategory:
        try:
            external_ref_category = ExternalPackageRefCategory[
                json_str_to_enum_name(external_ref_category_str)]
        except KeyError:
            raise SPDXParsingError([f"Category {external_ref_category_str} not valid for externalPackageRef."])

        return external_ref_category

    @staticmethod
    def parse_package_verification_code(verification_code_dict: Dict) -> PackageVerificationCode:
        excluded_files: List[str] = verification_code_dict.get("packageVerificationCodeExcludedFiles")
        verification_code_value: str = verification_code_dict.get("packageVerificationCodeValue")

        package_verification_code = construct_or_raise_parsing_error(PackageVerificationCode,
                                                                     dict(value=verification_code_value,
                                                                          excluded_files=excluded_files))

        return package_verification_code

    @staticmethod
    def parse_primary_package_purpose(primary_package_purpose: str) -> PackagePurpose:
        try:
            return PackagePurpose[json_str_to_enum_name(primary_package_purpose)]
        except KeyError:
            raise SPDXParsingError([f"Invalid primaryPackagePurpose: {primary_package_purpose}"])

    @staticmethod
    def parse_download_location(download_location: str) -> Union[str, SpdxNoAssertion, SpdxNone]:
        if download_location == SpdxNone().__str__():
            return SpdxNone()
        if download_location == SpdxNoAssertion().__str__():
            return SpdxNoAssertion()
        return download_location
