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
from enum import Enum, auto
from typing import Optional, Union, List

from src.model.actor import Actor
from src.model.checksum import Checksum
from src.model.license_expression import LicenseExpression
from src.model.spdx_no_assertion import SpdxNoAssertion
from src.model.spdx_none import SpdxNone


class PackagePurpose(Enum):
    APPLICATION = auto()
    FRAMEWORK = auto()
    LIBRARY = auto()
    CONTAINER = auto()
    OPERATING_SYSTEM = auto()
    DEVICE = auto()
    FIRMWARE = auto()
    SOURCE = auto()
    ARCHIVE = auto()
    FILE = auto()
    INSTALL = auto()
    OTHER = auto()


class PackageVerificationCode:
    value: str
    excluded_files: List[str]

    def __init__(self, value: str, excluded_files: List[str] = None):
        self.value = value
        self.excluded_files = excluded_files or []


class ExternalPackageReferenceCategory(Enum):
    SECURITY = auto()
    PACKAGE_MANAGER = auto()
    PERSISTENT_ID = auto()
    OTHER = auto()


class ExternalPackageReference:
    category: ExternalPackageReferenceCategory
    # In theory, once could refine the typing,
    # see https://spdx.github.io/spdx-spec/v2.3/external-repository-identifiers/. But it's probably not worth the
    # effort.
    reference_type: str
    locator: str
    comment: Optional[str]

    def __init__(self, category: ExternalPackageReferenceCategory, reference_type: str, locator: str,
                 comment: Optional[str] = None):
        self.category = category
        self.reference_type = reference_type
        self.locator = locator
        self.comment = comment


class Package:
    spdx_id: str
    name: str
    download_location: Union[str, SpdxNoAssertion, SpdxNone]
    version: Optional[str]
    file_name: Optional[str]
    supplier: Optional[Actor, SpdxNoAssertion]
    originator: Optional[Actor, SpdxNoAssertion]
    files_analyzed: bool  # defaults to True
    verification_code: Optional[PackageVerificationCode]
    checksums: List[Checksum]
    homepage: Optional[str, SpdxNoAssertion, SpdxNone]
    source_info: Optional[str]
    license_concluded: Optional[LicenseExpression, SpdxNoAssertion, SpdxNone]
    license_info_from_files: Optional[List[LicenseExpression], SpdxNoAssertion, SpdxNone]
    license_declared: Optional[LicenseExpression, SpdxNoAssertion, SpdxNone]
    license_comment: Optional[str]
    copyright_text: Optional[str, SpdxNoAssertion, SpdxNone]
    summary: Optional[str]
    description: Optional[str]
    comment: Optional[str]
    external_references: List[ExternalPackageReference]
    attribution_texts: List[str]
    primary_package_purpose: Optional[PackagePurpose]
    release_date: Optional[datetime]
    built_date: Optional[datetime]
    valid_until_date: Optional[datetime]

    def __init__(self, spdx_id: str, name: str, download_location: Union[str, SpdxNoAssertion, SpdxNone],
                 version: Optional[str] = None, file_name: Optional[str] = None,
                 supplier: Optional[Actor, SpdxNoAssertion] = None, originator: Optional[Actor, SpdxNoAssertion] = None,
                 files_analyzed: bool = True, verification_code: Optional[PackageVerificationCode] = None,
                 checksums: List[Checksum] = None, homepage: Optional[str, SpdxNoAssertion, SpdxNone] = None,
                 source_info: Optional[str] = None,
                 license_concluded: Optional[LicenseExpression, SpdxNoAssertion, SpdxNone] = None,
                 license_info_from_files: Optional[List[LicenseExpression], SpdxNoAssertion, SpdxNone] = None,
                 license_declared: Optional[LicenseExpression, SpdxNoAssertion, SpdxNone] = None,
                 license_comment: Optional[str] = None,
                 copyright_text: Optional[str, SpdxNoAssertion, SpdxNone] = None,
                 summary: Optional[str] = None, description: Optional[str] = None, comment: Optional[str] = None,
                 external_references: List[ExternalPackageReference] = None, attribution_texts: List[str] = None,
                 primary_package_purpose: Optional[PackagePurpose] = None, release_date: Optional[datetime] = None,
                 built_date: Optional[datetime] = None, valid_until_date: Optional[datetime] = None):
        self.spdx_id = spdx_id
        self.name = name
        self.download_location = download_location
        self.version = version
        self.file_name = file_name
        self.supplier = supplier
        self.originator = originator
        self.files_analyzed = files_analyzed
        self.verification_code = verification_code
        self.checksums = checksums
        self.homepage = homepage
        self.source_info = source_info
        self.license_concluded = license_concluded
        self.license_info_from_files = license_info_from_files
        self.license_declared = license_declared
        self.license_comment = license_comment
        self.copyright_text = copyright_text
        self.summary = summary
        self.description = description
        self.comment = comment
        self.external_references = external_references or []
        self.attribution_texts = attribution_texts or []
        self.primary_package_purpose = primary_package_purpose
        self.release_date = release_date
        self.built_date = built_date
        self.valid_until_date = valid_until_date
