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
from src.parser.json.dict_parsing_functions import append_list_if_object_could_be_parsed_append_logger_if_not, \
    datetime_from_str, parse_optional_field, raise_parsing_error_without_additional_text_if_logger_has_messages, \
    raise_parsing_error_if_logger_has_messages, \
    transform_json_str_to_enum_name, try_construction_raise_parsing_error, \
    try_parse_optional_field_append_logger_when_failing, try_parse_required_field_append_logger_when_failing
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
            packages_list = append_list_if_object_could_be_parsed_append_logger_if_not(logger=self.logger,
                                                                                       list_to_append=packages_list,
                                                                                       field=package_dict,
                                                                                       method_to_parse=self.parse_package)

        raise_parsing_error_without_additional_text_if_logger_has_messages(self.logger)

        return packages_list

    def parse_package(self, package_dict: Dict) -> Package:
        logger = Logger()
        name: str = package_dict.get("name")
        spdx_id: str = package_dict.get("SPDXID")
        attribution_texts: List[str] = package_dict.get("attributionTexts")

        built_date: Optional[datetime] = try_parse_optional_field_append_logger_when_failing(logger=logger,
                                                                                             field=package_dict.get(
                                                                                                 "builtDate"),
                                                                                             method_to_parse=datetime_from_str)

        checksums = try_parse_optional_field_append_logger_when_failing(logger=logger,
                                                                        field=package_dict.get("checksums"),
                                                                        method_to_parse=self.checksum_parser.parse_checksums)
        comment: Optional[str] = package_dict.get("comment")
        copyright_text: Optional[str] = package_dict.get("copyrightText")
        description: Optional[str] = package_dict.get("description")
        download_location: Union[str, SpdxNoAssertion, SpdxNone] = self.parse_download_location(
            package_dict.get("downloadLocation"))

        external_refs: List[ExternalPackageRef] = try_parse_optional_field_append_logger_when_failing(logger=logger,
                                                                                                      field=package_dict.get(
                                                                                                          "externalRefs"),
                                                                                                      method_to_parse=self.parse_external_refs)

        files_analyzed: Optional[bool] = parse_optional_field(package_dict.get("filesAnalyzed"), default=True)
        homepage: Optional[str] = package_dict.get("homepage")
        license_comments: Optional[str] = package_dict.get("licenseComments")
        license_concluded = try_parse_optional_field_append_logger_when_failing(logger, field=package_dict.get(
            "licenseConcluded"),
                                                                                method_to_parse=self.license_expression_parser.parse_license_expression,
                                                                                default=None)

        license_declared: Optional[
            Union[LicenseExpression, SpdxNoAssertion, SpdxNone]] = try_parse_optional_field_append_logger_when_failing(
            logger=logger, field=package_dict.get("licenseDeclared"),
            method_to_parse=self.license_expression_parser.parse_license_expression)

        license_info_from_file: Optional[
            Union[List[
                LicenseExpression], SpdxNoAssertion, SpdxNone]] = try_parse_optional_field_append_logger_when_failing(
            logger=logger, field=package_dict.get("licenseInfoFromFiles"),
            method_to_parse=self.license_expression_parser.parse_license_expression)

        originator: Optional[Union[Actor, SpdxNoAssertion]] = try_parse_optional_field_append_logger_when_failing(
            logger=logger, field=package_dict.get("originator"),
            method_to_parse=self.actor_parser.parse_actor_or_no_assert)

        package_file_name: Optional[str] = package_dict.get("packageFileName")

        package_verification_code: Optional[
            PackageVerificationCode] = try_parse_optional_field_append_logger_when_failing(logger=logger,
                                                                                           field=package_dict.get(
                                                                                               "packageVerificationCode"),
                                                                                           method_to_parse=self.parse_package_verification_code)
        primary_package_purpose: Optional[PackagePurpose] = try_parse_optional_field_append_logger_when_failing(
            logger=logger, field=package_dict.get("primaryPackagePurpose"),
            method_to_parse=self.parse_primary_package_purpose)

        release_date: Optional[datetime] = try_parse_optional_field_append_logger_when_failing(logger=logger,
                                                                                               field=package_dict.get(
                                                                                                   "releaseDate"),
                                                                                               method_to_parse=datetime_from_str)

        source_info: Optional[str] = package_dict.get("sourceInfo")
        summary: Optional[str] = package_dict.get("summary")
        supplier: Optional[Union[Actor, SpdxNoAssertion]] = try_parse_optional_field_append_logger_when_failing(
            logger=logger, field=package_dict.get("supplier"),
            method_to_parse=self.actor_parser.parse_actor_or_no_assert)

        valid_until_date: Optional[datetime] = try_parse_optional_field_append_logger_when_failing(logger=logger,
                                                                                                   field=package_dict.get(
                                                                                                       "validUntilDate"),
                                                                                                   method_to_parse=datetime_from_str)

        version_info: Optional[str] = package_dict.get("versionInfo")
        raise_parsing_error_if_logger_has_messages(logger, f"Package {name}")

        package = try_construction_raise_parsing_error(Package, dict(spdx_id=spdx_id, name=name,
                                                                     download_location=download_location,
                                                                     version=version_info,
                                                                     file_name=package_file_name, supplier=supplier,
                                                                     originator=originator,
                                                                     files_analyzed=files_analyzed,
                                                                     verification_code=package_verification_code,
                                                                     checksums=checksums, homepage=homepage,
                                                                     source_info=source_info,
                                                                     license_concluded=license_concluded,
                                                                     license_info_from_files=license_info_from_file,
                                                                     license_declared=license_declared,
                                                                     license_comment=license_comments,
                                                                     copyright_text=copyright_text, summary=summary,
                                                                     description=description,
                                                                     comment=comment, external_references=external_refs,
                                                                     attribution_texts=attribution_texts,
                                                                     primary_package_purpose=primary_package_purpose,
                                                                     release_date=release_date, built_date=built_date,
                                                                     valid_until_date=valid_until_date))

        return package

    def parse_external_refs(self, external_ref_dicts: List[Dict]) -> List[ExternalPackageRef]:
        external_refs = []
        for external_ref_dict in external_ref_dicts:
            external_refs = append_list_if_object_could_be_parsed_append_logger_if_not(logger=self.logger,
                                                                                       list_to_append=external_refs,
                                                                                       field=external_ref_dict,
                                                                                       method_to_parse=self.parse_external_ref)

        return external_refs

    def parse_external_ref(self, external_ref_dict: Dict) -> ExternalPackageRef:
        logger = Logger()
        ref_category = try_parse_required_field_append_logger_when_failing(logger=logger, field=external_ref_dict.get(
            "referenceCategory"), method_to_parse=self.parse_external_ref_category)
        ref_locator = external_ref_dict.get("referenceLocator")
        ref_type = external_ref_dict.get("referenceType")
        comment = external_ref_dict.get("comment")
        raise_parsing_error_if_logger_has_messages(logger, "external  ref")
        external_ref = try_construction_raise_parsing_error(ExternalPackageRef,
                                                            dict(category=ref_category, reference_type=ref_type,
                                                                 locator=ref_locator,
                                                                 comment=comment))

        return external_ref

    @staticmethod
    def parse_external_ref_category(external_ref_category_str: str) -> ExternalPackageRefCategory:
        try:
            external_ref_category = ExternalPackageRefCategory[
                transform_json_str_to_enum_name(external_ref_category_str)]
        except KeyError:
            raise SPDXParsingError([f"Category {external_ref_category_str} not valid for externalPackageRef."])

        return external_ref_category

    @staticmethod
    def parse_package_verification_code(verification_code_dict: Dict) -> PackageVerificationCode:
        excluded_files: List[str] = verification_code_dict.get("packageVerificationCodeExcludedFiles")
        verification_code_value: str = verification_code_dict.get("packageVerificationCodeValue")

        package_verification_code = try_construction_raise_parsing_error(PackageVerificationCode,
                                                                         dict(value=verification_code_value,
                                                                              excluded_files=excluded_files))

        return package_verification_code

    @staticmethod
    def parse_primary_package_purpose(primary_package_purpose: str) -> PackagePurpose:
        try:
            return PackagePurpose[transform_json_str_to_enum_name(primary_package_purpose)]
        except KeyError:
            raise SPDXParsingError([f"Invalid primaryPackagePurpose: {primary_package_purpose}"])

    @staticmethod
    def parse_download_location(download_location: str) -> Union[str, SpdxNoAssertion, SpdxNone]:
        if download_location == SpdxNone().__str__():
            return SpdxNone()
        if download_location == SpdxNoAssertion().__str__():
            return SpdxNoAssertion()
        return download_location
