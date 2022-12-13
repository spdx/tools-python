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
from typing import Dict, List, Optional

from src.model.checksum import Checksum
from src.model.package import Package, ExternalPackageRef, PackageVerificationCode, PackagePurpose, \
    ExternalPackageRefCategory
from src.model.typing.constructor_type_errors import ConstructorTypeErrors
from src.parser.error import SPDXParsingError
from src.parser.json.actor_parser import ActorParser
from src.parser.json.checksum_parser import ChecksumParser
from src.parser.json.dict_parsing_functions import datetime_from_str, parse_optional_field, \
    transform_json_str_to_enum_name
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

    def parse_package(self, package_dict: Dict) -> Package:
        name: str = package_dict.get("name")
        spdx_id: str = package_dict.get("SPDXID")
        attribution_texts: List[str] = package_dict.get("attributionTexts")
        try:
            built_date: Optional[datetime] = parse_optional_field(package_dict.get("builtDate"), datetime_from_str)
        except ValueError:
            self.logger.append("ValueError while parsing builtDate.")
            built_date = None
        try:
            checksums: List[Checksum] = parse_optional_field(package_dict.get("checksums"),
                                                             self.checksum_parser.parse_checksums)
        except SPDXParsingError as err:
            self.logger.append_all(err.get_messages())
            checksums = []
        comment: str = package_dict.get("comment")
        copyright_text: str = package_dict.get("copyrightText")
        description: str = package_dict.get("description")
        download_location: str = package_dict.get("downloadLocation")
        try:
            external_refs: List[ExternalPackageRef] = parse_optional_field(package_dict.get("externalRefs"),
                                                                           self.parse_external_refs)
        except SPDXParsingError as err:
            self.logger.append_all(err.get_messages())
            external_refs = []
        files_analyzed: bool = parse_optional_field(package_dict.get("filesAnalyzed"), default=True)
        homepage: str = package_dict.get("homepage")
        license_comments: str = package_dict.get("licenseComments")
        try:
            license_concluded = parse_optional_field(package_dict.get("licenseConcluded"),
                                                     self.license_expression_parser.parse_license_expression)
        except ConstructorTypeErrors as err:
            self.logger.append_all(err.get_messages())
            license_concluded = None
        try:
            license_declared = parse_optional_field(package_dict.get("licenseDeclared"),
                                                    self.license_expression_parser.parse_license_expression)
        except ConstructorTypeErrors as err:
            self.logger.append_all(err.get_messages())
            license_declared = None
        try:
            license_info_from_file = parse_optional_field(package_dict.get("licenseInfoFromFiles"),
                                                          self.license_expression_parser.parse_license_expression)
        except ConstructorTypeErrors as err:
            self.logger.append_all(err.get_messages())
            license_info_from_file = None
        try:
            originator = parse_optional_field(package_dict.get("originator"), self.actor_parser.parse_actor)
        except SPDXParsingError as err:
            self.logger.append_all(err.get_messages())
            originator = None
        package_file_name: str = package_dict.get("packageFileName")
        try:
            package_verification_code: Optional[PackageVerificationCode] = parse_optional_field(
                package_dict.get("packageVerificationCode"), self.parse_package_verification_code)
        except SPDXParsingError as err:
            self.logger.append_all(err.get_messages())
            package_verification_code = None

        try:
            primary_package_purpose: Optional[PackagePurpose] = parse_optional_field(
                package_dict.get("primaryPackagePurpose"), self.parse_primary_package_purpose)
        except SPDXParsingError as err:
            self.logger.append_all(err.get_messages())
            primary_package_purpose = None

        try:
            release_date: Optional[datetime] = parse_optional_field(package_dict.get("releaseDate"), datetime_from_str)
        except ValueError:
            self.logger.append("ValueError while parsing releaseDate.")
            release_date = None
        source_info: str = package_dict.get("sourceInfo")
        summary: str = package_dict.get("summary")
        try:
            supplier = parse_optional_field(package_dict.get("supplier"), self.actor_parser.parse_actor)
        except SPDXParsingError as err:
            self.logger.append_all(err.get_messages())
            supplier = None
        try:
            valid_until_date = parse_optional_field(package_dict.get("validUntilDate"), datetime_from_str)
        except ValueError:
            self.logger.append("ValueError while parsing validUntilDate.")
            valid_until_date = None

        version_info: str = package_dict.get("versionInfo")
        if self.logger.has_messages():
            raise SPDXParsingError(self.logger.get_messages())
        # flush logger? parser for each package?

        try:
            package = Package(spdx_id=spdx_id, name=name, download_location=download_location, version=version_info,
                              file_name=package_file_name, supplier=supplier, originator=originator,
                              files_analyzed=files_analyzed,
                              verification_code=package_verification_code, checksums=checksums, homepage=homepage,
                              source_info=source_info,
                              license_concluded=license_concluded, license_info_from_files=license_info_from_file,
                              license_declared=license_declared,
                              license_comment=license_comments, copyright_text=copyright_text, summary=summary,
                              description=description,
                              comment=comment, external_references=external_refs, attribution_texts=attribution_texts,
                              primary_package_purpose=primary_package_purpose,
                              release_date=release_date, built_date=built_date, valid_until_date=valid_until_date)

        except ConstructorTypeErrors as err:
            self.logger.append_all(err.get_messages())
            raise SPDXParsingError(self.logger.get_messages())

        return package

    def parse_packages(self, packages_dict_list: List[Dict]) -> List[Package]:
        packages_list = []
        for package_dict in packages_dict_list:
            try:
                package = self.parse_package(package_dict)
                packages_list.append(package)
            except SPDXParsingError as err:
               # self.logger.append_all(err.get_messages())
                continue
        if self.logger.has_messages():
            raise SPDXParsingError(self.logger.get_messages())

        return packages_list

    def parse_external_refs(self, external_ref_dicts: List[Dict]) -> List[ExternalPackageRef]:
        external_refs = []
        for external_ref_dict in external_ref_dicts:
            try:
                external_ref = self.parse_external_ref(external_ref_dict)
                external_refs.append(external_ref)
            except SPDXParsingError as err:
                self.logger.append_all(err.get_messages())
        return external_refs

    def parse_external_ref(self, external_ref_dict: Dict) -> ExternalPackageRef:
        ref_category = external_ref_dict.get("referenceCategory")
        try:
            ref_category = ExternalPackageRefCategory[ref_category.replace("-","_")]
        except KeyError:
            raise SPDXParsingError([f"Category {ref_category} not valid for externalPackageRef."])
        ref_locator = external_ref_dict.get("referenceLocator")
        ref_type = external_ref_dict.get("referenceType")
        comment = external_ref_dict.get("comment")
        try:
            external_ref = ExternalPackageRef(category=ref_category, reference_type=ref_type, locator=ref_locator,
                                              comment=comment)
        except ConstructorTypeErrors as err:
            raise SPDXParsingError([f"Error while parsing external ref: {err.get_messages()}"])

        return external_ref

    def parse_package_verification_code(self, verification_code_dict: Dict) -> PackageVerificationCode:
        excluded_files: List[str] = verification_code_dict.get("packageVerificationCodeExcludedFiles")
        verification_code_value: str = verification_code_dict.get("packageVerificationCodeValue")
        try:
            package_verification_code = PackageVerificationCode(value=verification_code_value,
                                                                excluded_files=excluded_files)
        except ConstructorTypeErrors as err:
            raise SPDXParsingError([f"Error while parsing package verification code: {err.get_messages()}"])

        return package_verification_code

    def parse_primary_package_purpose(self, primary_package_purpose: str) -> PackagePurpose:
        try:
            return PackagePurpose[transform_json_str_to_enum_name(primary_package_purpose)]
        except KeyError:
            raise SPDXParsingError([f"Invalid primaryPackagePurpose: {primary_package_purpose}"])

