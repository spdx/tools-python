#  Copyright (c) 2022 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from datetime import datetime

from src.model.actor import Actor, ActorType
from src.model.checksum import Checksum, ChecksumAlgorithm
from src.model.document import CreationInfo
from src.model.external_document_ref import ExternalDocumentRef
from src.model.file import File, FileType
from src.model.license_expression import LicenseExpression
from src.model.package import Package, PackageVerificationCode, PackagePurpose
from src.model.version import Version

"""Utility methods to create data model instances. All properties have valid defaults, so they don't need to be 
specified unless relevant for the test."""


def creation_info_fixture(spdx_version="spdxVersion", spdx_id="documentId", name="documentName",
                          namespace="documentNamespace", creators=None, created=datetime(2022, 12, 1),
                          creator_comment="creatorComment", data_license="CC0-1.0", external_document_refs=None,
                          license_list_version=Version(3, 19), document_comment="documentComment") -> CreationInfo:
    creators = [Actor(ActorType.PERSON, "creatorName")] if creators is None else creators
    external_document_refs = [
        external_document_ref_fixture()] if external_document_refs is None else external_document_refs
    return CreationInfo(spdx_version, spdx_id, name, namespace, creators, created, creator_comment, data_license,
                        external_document_refs, license_list_version, document_comment)


def file_fixture(name="fileName", spdx_id="fileId", checksums=None, file_type=None,
                 concluded_license=LicenseExpression("concludedLicenseExpression"), license_info_in_file=None,
                 license_comment="licenseComment", copyright_text="copyrightText", comment="fileComment",
                 notice="fileNotice", contributors=None, attribution_texts=None) -> File:
    checksums = [Checksum(ChecksumAlgorithm.SHA1, "sha1")] if checksums is None else checksums
    file_type = [FileType.TEXT] if file_type is None else file_type
    license_info_in_file = [
        LicenseExpression("licenseInfoInFileExpression")] if license_info_in_file is None else license_info_in_file
    contributors = ["fileContributor"] if contributors is None else contributors
    attribution_texts = ["fileAttributionText"] if attribution_texts is None else attribution_texts
    return File(name=name, spdx_id=spdx_id, checksums=checksums, file_type=file_type,
                concluded_license=concluded_license, license_info_in_file=license_info_in_file,
                license_comment=license_comment, copyright_text=copyright_text, comment=comment, notice=notice,
                contributors=contributors, attribution_texts=attribution_texts)


def package_fixture(spdx_id="packageId", name="packageName", download_location="downloadLocation",
                    version="packageVersion", file_name="packageFileName",
                    supplier=Actor(ActorType.PERSON, "supplierName"),
                    originator=Actor(ActorType.PERSON, "originatorName"), files_analyzed=True,
                    verification_code=PackageVerificationCode("verificationCode"), checksums=None,
                    homepage="packageHomepage", source_info="sourceInfo",
                    license_concluded=LicenseExpression("packageLicenseConcluded"), license_info_from_files=None,
                    license_declared=LicenseExpression("packageLicenseDeclared"),
                    license_comment="packageLicenseComment", copyright_text="packageCopyrightText",
                    summary="packageSummary", description="packageDescription", comment="packageComment",
                    external_references=None, attribution_texts=None, primary_package_purpose=PackagePurpose.SOURCE,
                    release_date=datetime(2022, 12, 1), built_date=datetime(2022, 12, 2),
                    valid_until_date=datetime(2022, 12, 3)) -> Package:
    checksums = [Checksum(ChecksumAlgorithm.SHA1, "packageSha1")] if checksums is None else checksums
    license_info_from_files = [
        LicenseExpression("licenseInfoFromFile")] if license_info_from_files is None else license_info_from_files
    external_references = [] if external_references is None else external_references
    attribution_texts = ["packageAttributionText"] if attribution_texts is None else attribution_texts
    return Package(spdx_id=spdx_id, name=name, download_location=download_location, version=version,
                   file_name=file_name, supplier=supplier, originator=originator, files_analyzed=files_analyzed,
                   verification_code=verification_code, checksums=checksums, homepage=homepage, source_info=source_info,
                   license_concluded=license_concluded, license_info_from_files=license_info_from_files,
                   license_declared=license_declared, license_comment=license_comment, copyright_text=copyright_text,
                   summary=summary, description=description, comment=comment, external_references=external_references,
                   attribution_texts=attribution_texts, primary_package_purpose=primary_package_purpose,
                   release_date=release_date, built_date=built_date, valid_until_date=valid_until_date)


def external_document_ref_fixture(document_ref_id="externalDocumentRefId", document_uri="externalDocumentUri",
                                  checksum=Checksum(ChecksumAlgorithm.MD5,
                                                    "externalDocumentRefMd5")) -> ExternalDocumentRef:
    return ExternalDocumentRef(document_ref_id=document_ref_id, document_uri=document_uri, checksum=checksum)
